package server

import (
	"context"
	"errors"
	"fmt"
	"log"
	"os"
	"syscall"

	etree "github.com/beevik/etree"
	"math/rand"
	"strconv"

	"os/exec"

	"github.com/google/uuid"

	pb "github.com/gabroo/evomorph/protos/go"
)

const (
	SCRIPT_PATH = "engine/server/run.sh"
	LOG_FILE    = "morpheus.log"
)

type service struct {
	pb.UnimplementedEngineServer                        // base engine server
	jobs                         map[string]*os.Process // map of jobs by id
}

func New() (*service, error) {
	srv := &service{
		jobs: map[string]*os.Process{},
	}
	return srv, nil
}

// Engine:Start(ModelPath, OutDir)
func (s *service) Start(ctx context.Context, rq *pb.StartRequest) (*pb.StartReply, error) {
	if s.jobs == nil {
		return nil, errors.New("s.jobs is nil in Start")
	}

	model, out := rq.Model, rq.Out
	id, err := startJob(model, out, s.jobs)

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
	return rp, err
}

// Top-level runner; executes simulations and invokes file watcher.
func startJob(model string, out string, jobs map[string]*os.Process) (string, error) {
	// each job gets a UUID
	id := uuid.New().String()
	if id == "" {
		return id, errors.New("uuid generation failed")
	}

	// ensure output directory exists
	out += fmt.Sprintf("/%s", id)
	if err := os.MkdirAll(out, 0777); err != nil {
		return id, err
	}

	// Load model
	doc := etree.NewDocument()
	if err := doc.ReadFromFile(model); err != nil {
		panic(err)
	}

	// Random number placeholders for now
	a_cells := rand.Intn(101)
	b_cells := rand.Intn(101)

	// Find each number-of-cells attribute and set value
	for _, e := range doc.FindElements("//Population") {
		if e.SelectAttrValue("type", "") == "A"{
			e.SelectElement("InitCircle").SelectAttr("number-of-cells").Value = strconv.Itoa(a_cells)
		}
		if e.SelectAttrValue("type", "") == "B"{
			e.SelectElement("InitCircle").SelectAttr("number-of-cells").Value = strconv.Itoa(b_cells)
		}
	}

	// Write to output directory
	doc.WriteToFile(out + "/three_layer_modified")

	// we invoke Morpheus via shell script
	sh, err := exec.LookPath(SCRIPT_PATH)
	if err != nil {
		return id, err
	}
	
	// Change model path to individual simulation's modified xml
	model = out + "/three_layer_modified"
	
	cmd := exec.Command(sh, "-i", model, "-o", out)
	logfile := fmt.Sprintf("%s/%s", out, LOG_FILE)
	file, err := os.Create(logfile)
	if err != nil {
		return id, err
	}

	cmd.Stdout = file
	cmd.Stderr = file
	if err = cmd.Start(); err != nil {
		return id, err
	}

	// make sure the job is cleared from
	go func() {
		err := cmd.Wait()
		if err == nil {
			stopJob(id, jobs)
		}
	}()

	jobs[id] = cmd.Process
	log.Printf("START (%s): length %d\n", id, len(jobs))
	return id, err
}

// Engine:Stop(Uuid)
func (s *service) Stop(ctx context.Context, rq *pb.Simulation) (*pb.Status, error) {
	// select appropriate status
	if s.jobs == nil {
		return nil, errors.New("s.jobs is nil in stopJob()")
	}

	status := pb.StatusType_OK
	err := stopJob(rq.Uuid, s.jobs)
	if err != nil {
		status = pb.StatusType_ERROR
	}

	// make and send response
	rp := &pb.Status{Status: status}
	return rp, err
}

// stops job with `id` and removes from `jobs`
func stopJob(id string, jobs map[string]*os.Process) error {
	c, ok := jobs[id]
	if !ok {
		return fmt.Errorf("id %s not in jobs", id)
	}

	delete(jobs, id)
	log.Printf("STOP (%s): length %d\n", id, len(jobs))

	// TODO verify which signal to send
	// https://www.baeldung.com/linux/sigint-and-other-termination-signals
	if err := c.Signal(syscall.SIGQUIT); err != nil {
		return err
	}
	return nil
}
