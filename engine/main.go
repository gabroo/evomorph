package main

import (
	"log"
	"net"

  pb "evomorph/protos"
	"google.golang.org/grpc"

  "github.com/gabroo/evomorph/engine/server"
)

const (
	HOST = "localhost"
	PORT = ":50051"
	ADDR = HOST + PORT
)

func main() {
	log.Printf("starting server ...\n")
	lis, err := net.Listen("tcp", ADDR)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	pb.RegisterEngineServer(s, &server.Service{})

	log.Printf("server listening at %v\n\n", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to server: %v", err)
	}
}
