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

	pb "github.com/gabroo/evomorph/protos/go"

	"github.com/google/uuid"
)

const (
	// Delay between poll iterations for file watching.
	INTERVAL = 100 * time.Millisecond
)

type Service struct {
	pb.UnimplementedEngineServer                       // base engine server
	jobs                         map[string]chan error // job queue with channels
}

// Engine:Start(ModelPath, OutDir)
func (s *Service) Start(ctx context.Context, rq *pb.StartRequest) (*pb.StartReply, error) {
	// check job queue (TODO) better way to do this?
	if s.jobs == nil {
		s.jobs = make(map[string]chan error)
	}

	models, out := rq.Models, rq.Out
	id, err := startJob(models, out, s.jobs)

	// select appropriate status
	status := pb.StatusType_OK
	if err != nil {
		status = pb.StatusType_ERROR
		log.Printf("error in Start: %v", err)
	}

	// make and send response
	rp := &pb.StartReply{
		Status: status,
		Uuid:   id,
	}
	fmt.Printf("\tsending back uuid\n\n")
	return rp, nil
}

// Top-level runner; executes simulations and invokes file watcher.
func startJob(models []string, out string, jobs map[string]chan error) (string, error) {
	// each job gets a UUID
	id := uuid.New().String()
	if id == "" {
		return id, errors.New("uuid generation failed")
	}

	out += fmt.Sprintf("/%s", id)
	if err := os.MkdirAll(out, 0777); err != nil {
		return id, err
	}

	// we invoke Morpheus via shell script
	sh, err := exec.LookPath("engine/server/run.sh")
	if err != nil {
		return id, err
	}

	// every sim for this job shares the same start/stop channel
	start, stop := make(chan *os.Process), make(chan error)
	jobs[id] = stop

	// each sim gets a command
	for _, model := range models {
		cmd := exec.Command(sh, "-i", model, "-o", out)
		fmt.Printf("\tadded (%s) to queue (length %d)\n", id, len(jobs))

		// start command and watch for output files
		go executeCmd(cmd, start, stop, out+"/morpheus.log")
		go watchFiles(out, stop, id)
	}
	return id, err
}

// Start command and signal on start channel, then wait for command to complete and signal on stop channel.
func executeCmd(
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
	if err = cmd.Start(); err != nil {
		stop <- err
	}

	// start <- cmd.Process
	err = cmd.Wait()
	stop <- err
}

// Iterates filepaths in `dir` and adds them to map `seen`.
// Watches files in out dir and prints when finds new ones.
func watchFiles(
	out string,
	stop <-chan error,
	id string,
) error {
	seen := make(map[string]bool)
	log.Printf("watching files for (%s)...", id)
	log.Printf("out: %s", out)

	// Files not in `seen` are printed
	scanFiles := func(dir string) error {
		files, err := os.ReadDir(dir)
		if err != nil {
			return err
		}

		for _, f := range files {
			name := f.Name()
			// (TODO) fix this png magic string
			if strings.HasSuffix(name, ".png") && !seen[name] {
				fmt.Printf("\t%s\n", name)
				seen[name] = true
			}
		}

		return nil
	}

	// (TODO) this is polling, ideally we can listen for events?
	for {
		select {
		case err := <-stop:
			return err
		default:
			scanFiles(out)
			time.Sleep(INTERVAL)
		}
	}
}

// Engine:Stop(Uuid)
func (s *Service) Stop(ctx context.Context, rq *pb.StopRequest) (*pb.Status, error) {
	// select appropriate status
	status := pb.StatusType_OK
	if err := stopJob(rq.Uuid, s.jobs); err != nil {
		status = pb.StatusType_ERROR
	}

	// make and send response
	rp := &pb.Status{Status: status}
	return rp, nil
}

// stops job with `id` and removes from `jobs` queue
func stopJob(id string, jobs map[string]chan error) error {
	if jobs == nil {
		return errors.New("jobs is nil")
	}

	c := jobs[id]
	c <- nil
	delete(jobs, id)
	return nil
}
