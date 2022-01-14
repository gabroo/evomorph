package main

import (
	"context"
	"log"
	"net"

	"google.golang.org/grpc"

	"github.com/gabroo/evomorph/controller/gateway"
	"github.com/gabroo/evomorph/controller/server"
	pb "github.com/gabroo/evomorph/protos/go"
)

const (
	ADDR = "0.0.0.0:50052"
)

func main() {
	log.Println("starting controller")
	lis, err := net.Listen("tcp", ADDR)
	if err != nil {
		log.Fatal("failed to listen:", err)
	}
	s := grpc.NewServer()
	srv, err := server.New()
	if err != nil {
		log.Fatal("failed to create server:", err)
	}
	pb.RegisterControllerServer(s, srv)

	go func() {
		log.Println("gRPC server listening:", lis.Addr())
		if err := s.Serve(lis); err != nil {
			log.Fatal("server failed:", err)
		}
	}()

	ctx := context.Background()
	log.Fatal(gateway.Run(ctx))
}
