package server

import (
	"context"
	"errors"
	"fmt"
	"log"
	"os"
	"os/exec"
	"strings"
	"time"

	pb "evomorph/protos"

	"github.com/google/uuid"
)

const (
	interval = 100 * time.Millisecond
)

type Service struct {
	pb.UnimplementedEngineServer
	jobs map[string]chan error
}

// Engine:Start(ModelPath, OutDir)
func (s *Service) Start(ctx context.Context, rq *pb.StartRequest) (*pb.StartReply, error) {
	log.Printf("called Start\n\tmodel path: %s\n\toutput directory: %s", rq.ModelPath, rq.OutDir)

	// check job queue (TODO) better way to do this?
	if s.jobs == nil {
		s.jobs = make(map[string]chan error)
	}

	in, out := rq.ModelPath, rq.OutDir
	id, err := run(in, out, s.jobs)

	// select appropriate status
	status := pb.StatusType_OK
	if err != nil {
		status = pb.StatusType_ERROR
		log.New(os.Stdout, "[WARNING] ", 0).Printf("error in Start: %v", err)
	}

	// make and send response
	rp := &pb.StartReply{Status: status, Uuid: id}
	fmt.Printf("\tsending back uuid\n\n")
	return rp, nil
}

// Engine:Stop(Uuid)
func (s *Service) Stop(ctx context.Context, rq *pb.StopRequest) (*pb.Status, error) {
	log.Printf("called Stop\n\tuuid: %s", rq.Uuid)

	err := stop(rq.Uuid, s.jobs)

	// select appropriate status
	status := pb.StatusType_OK
	if err != nil {
		status = pb.StatusType_ERROR
	}

	// make and send response
	rp := &pb.Status{Status: status}
	return rp, nil
}

// Watches files in out dir and prints when finds new ones.
// (TODO) this is polling, ideally we can listen for events?
func watch(
	out string,
	start <-chan *os.Process,
	stop <-chan error,
	jobs map[string]chan error,
	id string,
) error {
	seen := make(map[string]bool)
  log.Printf("scanning files for (%s)...", id)
	var p *os.Process
	for {
		select {
		case p = <-start:
			continue
		case err := <-stop:
      fmt.Printf("\tstopping (%s)\n", id) 
			delete(jobs, id)
      fmt.Printf("\tremoved from queue (length %d)\n", len(jobs))
			if p != nil {
				p.Kill()
			}
			return err
		default:
			files, err := os.ReadDir(out)
			if err != nil {
				return err
			}
			for _, f := range files {
				name := f.Name()
				if strings.HasSuffix(name, ".png") && !seen[name] {
					fmt.Printf("\t%s\n", name)
					seen[name] = true
				}
			}
			time.Sleep(interval)
		}
	}
}

// Waits for the command to complete and signal on channel.
func wait(
	cmd *exec.Cmd,
	start chan<- *os.Process,
	stop chan<- error,
	logfile string,
) {
	file, err := os.Create(logfile)
	if err != nil {
		stop <- err
	}
	cmd.Stdout = file
	err = cmd.Start()
	if err != nil {
		stop <- err
	}
	start <- cmd.Process
	err = cmd.Wait()
	stop <- err
}

// Runs simulation and invokes file watcher.
func run(in string, out string, jobs map[string]chan error) (string, error) {
	// each simulation gets a UUID
	id := uuid.New().String()
	if id == "" {
		return id, errors.New("uuid generation failed")
	}

	out += fmt.Sprintf("/%s", id)
	err := os.MkdirAll(out, 0777)
	if err != nil {
		return id, err
	}

	// we invoke Morpheus via shell script
	sh, err := exec.LookPath("engine/server/run.sh")
	if err != nil {
		return id, err
	}
	cmd := exec.Command(sh, "-i", in, "-o", out)
	start, stop := make(chan *os.Process), make(chan error)

	// add job to queue
	jobs[id] = stop
	fmt.Printf("\tadded (%s) to queue (length %d)\n", id, len(jobs))

	// start command and watch for output files
	go wait(cmd, start, stop, out+"/morpheus.log")
	go watch(out, start, stop, jobs, id)

	return id, err
}

// stops job with `id` and removes from `jobs` queue
func stop(id string, jobs map[string]chan error) error {
	if jobs == nil {
		return errors.New("jobs is nil")
	}
	c := jobs[id]
	c <- nil
	delete(jobs, id)
	return nil
}
