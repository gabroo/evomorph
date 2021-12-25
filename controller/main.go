package main

import (
	"log"
	"net"

	"google.golang.org/grpc"

	"github.com/gabroo/evomorph/controller/server"
	pb "github.com/gabroo/evomorph/protos/go"
)

const (
	HOST = "localhost"
	PORT = ":50052"
	ADDR = HOST + PORT
)

func main() {
	log.Println("starting controller")
	lis, err := net.Listen("tcp", ADDR)
	if err != nil {
		log.Fatalln("failed to listen:", err)
	}
	s := grpc.NewServer()
	pb.RegisterControllerServer(s, &server.Service{})

	log.Println("server listening:", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalln("server failed:", err)
	}
}
