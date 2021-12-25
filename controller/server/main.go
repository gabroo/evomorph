package server

import (
	"context"

	pb "github.com/gabroo/evomorph/protos/go"
)

type Service struct {
	pb.UnimplementedControllerServer          // base controller server
	jobs                             []string // list of jobs
}

func (s *Service) Run(ctx context.Context, rq *pb.RunRequest) (*pb.RunReply, error) {
	return nil, nil
}

func (s *Service) Pause(ctx context.Context, rq *pb.Simulation) (*pb.Status, error) {
	return nil, nil
}

func (s *Service) Resume(ctx context.Context, rq *pb.Simulation) (*pb.Status, error) {
	return nil, nil
}

func (s *Service) Cancel(ctx context.Context, rq *pb.Simulation) (*pb.Status, error) {
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
