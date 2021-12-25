package main

import (
	"context"
	"log"
	"path/filepath"
	"time"

	pb "github.com/gabroo/evomorph/protos/go"

	"google.golang.org/grpc"
)

const (
	ADDR = "localhost:50051"
	BASE = "./"
)

func main() {
	// Set up a connection to the server.
	conn, err := grpc.Dial(ADDR, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}

	// Contact the server and print out its response.
	c := pb.NewControllerClient(conn)
	log.Print("starting client...")

	// input and output files
	in, err := filepath.Abs(filepath.Join(BASE, "models/three_layer.xml"))
	if err != nil {
		log.Fatal(err)
	}
	out, err := filepath.Abs(filepath.Join(BASE, "out"))
	if err != nil {
		log.Fatal(err)
	}

	// Listen for messages
	ctx, cancel := context.WithTimeout(context.Background(), time.Minute)
	defer cancel()

	log.Print("calling Start")
	rp, err := c.Run(
		ctx,
		&pb.RunRequest{
      :     []string{in},
			Replicates: 1,
			Out:        out,
		},
	)
	if err != nil {
		log.Fatal(err)
	}
	log.Printf("response: %v", rp)
}
