package server

import (
	"context"
	"errors"
	"fmt"
	"log"
	"os"
	"strings"
	"time"

	"google.golang.org/grpc"

	pb "github.com/gabroo/evomorph/protos/go"
)

const (
	ENGINE_ADDR = "0.0.0.0:50051"
	BASE        = "./"

	// Delay between poll iterations for file watching.
	INTERVAL = 100 * time.Millisecond
)

type Service struct {
	pb.UnimplementedControllerServer                 // base controller server
	jobs                             []string        // list of jobs
	c                                pb.EngineClient // client for engine
}

func New() (*Service, error) {
	// connect to engine
	log.Print("creating engine client")
	conn, err := grpc.Dial(ENGINE_ADDR, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		return nil, err
	}
	s := &Service{}
	s.c = pb.NewEngineClient(conn)
	return s, nil
}

func startJob(c pb.EngineClient, in, out string, rq *pb.RunRequest) (string, error) {
	ctx, cancel := context.WithTimeout(context.Background(), time.Minute)
	defer cancel()
	rp, err := c.Start(
		ctx,
		&pb.StartRequest{
			Model: in,
			Out:   out,
			Params: rq.Params,
		},
	)
	if err != nil {
		log.Printf("error: %v", err)
		return "", err
	}
	log.Printf("response: %v", rp)
	return rp.Uuid, nil
}

func (s *Service) Run(ctx context.Context, rq *pb.RunRequest) (*pb.RunReply, error) {
	if s.c == nil {
		return nil, errors.New("nil engine client in controller server")
	}
	
	id, err := startJob(s.c, "models/barkley3d_coupling.xml", "out", rq)
	var status pb.StatusType
	if err != nil {
		status = pb.StatusType_ERROR
	} else {
		status = pb.StatusType_OK
		s.jobs = append(s.jobs, id)
	}
	rp := &pb.RunReply{
		Status: status,
		Uuid:   id,
	}
	return rp, err
}

func (s *Service) Cancel(ctx context.Context, rq *pb.Simulation) (*pb.Status, error) {
	id := rq.Uuid
	var status pb.StatusType
	if id == "" {
		status = pb.StatusType_ERROR
	} else {
		status = pb.StatusType_OK
	}
	if s.c == nil {
		return nil, errors.New("nil engine client in controller server")
	}
	ct, cancel := context.WithTimeout(context.Background(), time.Minute)
	defer cancel()
	rp, err := s.c.Stop(
		ct,
		&pb.Simulation{
			Uuid: id,
		},
	)
	if err != nil {
		log.Printf("error: %v", err)
		return nil, err
	}
	log.Printf("response: %v", rp)
	rp = &pb.Status{Status: status}
	return rp, nil
}

func (s *Service) Pause(ctx context.Context, rq *pb.Simulation) (*pb.Status, error) {
	return nil, nil
}

func (s *Service) Resume(ctx context.Context, rq *pb.Simulation) (*pb.Status, error) {
	return nil, nil
}

func (s *Service) GetStatus(ctx context.Context, rq *pb.Simulation) (*pb.Status, error) {
	return nil, nil
}

func (s *Service) GetProgress(ctx context.Context, rq *pb.Simulation) (*pb.Progress, error) {
	return nil, nil
}

func (s *Service) GetPictures(rq *pb.Simulation, stream pb.Controller_GetPicturesServer) error {
	return nil
}

func (s *Service) GetStructures(rq *pb.Simulation, stream pb.Controller_GetStructuresServer) error {
	return nil
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
