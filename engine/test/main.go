package main

import (
	"context"
	"fmt"
	"log"
	"time"

	pb "evomorph/protos"

	"google.golang.org/grpc"
)

const (
	address = "localhost:50051"
)

func main() {
	log.Printf("starting client...\npress <Enter> to send a request\n")
	var s string
	for {
		// Read line
		fmt.Scanln(&s)

		// Set up a connection to the server.
		conn, err := grpc.Dial(address, grpc.WithInsecure(), grpc.WithBlock())
		if err != nil {
			log.Fatalf("did not connect: %v", err)
		}

		// Contact the server and print out its response.
		c := pb.NewEngineClient(conn)
		ctx, cancel := context.WithTimeout(context.Background(), time.Second)
    log.Printf("calling Start")
		r, err := c.Start(ctx, &pb.StartRequest{ModelPath: "in", OutDir: "out"})
		cancel()
		if err != nil {
			log.Fatalf("error: %v", err)
		}
		log.Printf("response: %v", r)
	}
}
