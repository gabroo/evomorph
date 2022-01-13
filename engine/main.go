package main

import (
	"log"
	"net"

	"google.golang.org/grpc"

	"github.com/gabroo/evomorph/engine/server"
	pb "github.com/gabroo/evomorph/protos/go"
)

const (
	ADDR = "0.0.0.0:50051"
)

func main() {
	log.Println("starting engine")
	lis, err := net.Listen("tcp", ADDR)
	if err != nil {
		log.Fatalln("failed to listen:", err)
	}
	s := grpc.NewServer()
	srv, err := server.New()
	if err != nil {
		log.Fatal(err)
	}
	pb.RegisterEngineServer(s, srv)

	log.Println("server listening:", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalln("server failed:", err)
	}
}
