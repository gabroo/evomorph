package main

import (
	"log"
	"net"

  pb "evomorph/protos"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"

  "github.com/gabroo/evomorph/engine/server"
)

const (
	host = "localhost"
	port = ":50051"
	addr = host + port
)

func main() {
	log.Printf("starting server ...\n")
	lis, err := net.Listen("tcp", addr)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	pb.RegisterEngineServer(s, &server.Service{})
	reflection.Register(s)

	log.Printf("server listening at %v\n\n", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to server: %v", err)
	}
}
