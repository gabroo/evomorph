package main

import (
	"context"
	"fmt"
	"log"
	"time"

	fp "path/filepath"

	pb "github.com/gabroo/evomorph/protos/go"

	"google.golang.org/grpc"
)

const (
	ADDR = "0.0.0.0:50051"
	BASE = "./"
)

func main() {
	// Set up a connection to the server.
	conn, err := grpc.Dial(ADDR, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}

	// Contact the server and print out its response.
	c := pb.NewEngineClient(conn)
	log.Print("starting client...")
	log.Print("type 's' to start, 'p' to stop")

	// input and output files
	in, err := fp.Abs(fp.Join(BASE, "models/three_layer.xml"))
	if err != nil {
		log.Fatal(err)
	}
	out, err := fp.Abs(fp.Join(BASE, "out"))
	if err != nil {
		log.Fatal(err)
	}

	// Listen for messages
	id := ""
	var s string
	for {
		_, err := fmt.Scan(&s)
		if err != nil {
			log.Fatal(err)
			return
		}
		ctx, cancel := context.WithTimeout(context.Background(), time.Minute)
		defer cancel()

		switch s {
		case "s":
			log.Print("calling Start")
			rp, err := c.Start(
				ctx,
				&pb.StartRequest{
					Models:     []string{in},
					Replicates: 1,
					Out:        out,
				},
			)
			if err != nil {
				log.Fatal(err)
			}
			log.Printf("response: %v", rp)
			id = rp.Uuid
		case "p":
			if id == "" {
				log.Printf("no simulation started yet")
				continue
			}
			log.Printf("calling Stop(%s)", id)
			rp, err := c.Stop(
				ctx,
				&pb.Simulation{Uuid: id},
			)
			if err != nil {
				log.Fatal(err)
			}
			log.Printf("response: %v", rp)
		default:
			log.Print("type 's' to start, 'p' to stop")
		}
	}
}
