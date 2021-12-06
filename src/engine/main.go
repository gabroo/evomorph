package main

import (
	"context"
	"log"
	"net"

	pb "evomorph/protos"

	"google.golang.org/grpc"
)

const (
	host = "localhost"
	port = ":50051"
	addr = host + port
)

type server struct {
	pb.UnimplementedEngineServer
}

// Engine:Start
func (s *server) Start(ctx context.Context, in *pb.StartRequest) (*pb.StartReply, error) {
	log.Printf("called Start")
	log.Printf("received payload: %v", in)
	r := &pb.StartReply{Status: pb.StatusType_OK, Id: 123}
	log.Printf("sending back: %v", r)
	return r, nil
}

// Engine:Stop
func (s *server) Stop(ctx context.Context, in *pb.StopRequest) (*pb.Status, error) {
	log.Printf("called Stop")
	log.Printf("received payload: %v", in)
	r := &pb.Status{Status: pb.StatusType_OK}
	log.Printf("sending back: %v", r)
	return r, nil
}

func main() {
	log.Printf("starting server ...\n")
	lis, err := net.Listen("tcp", addr)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	pb.RegisterEngineServer(s, &server{})
	log.Printf("server listening at %v", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to server: %v", err)
	}
}
