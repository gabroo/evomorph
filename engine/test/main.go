package main

import (
	"context"
	"fmt"
	"log"
	"path/filepath"
	"time"

	pb "evomorph/protos"

	"google.golang.org/grpc"
)

const (
	ADDRESS       = "localhost:50051"
	STRESS_TEST_N = 50
)

func main() {
	// Set up a connection to the server.
	conn, err := grpc.Dial(ADDRESS, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}

	// Contact the server and print out its response.
	c := pb.NewEngineClient(conn)
	log.Printf("starting client...\ntype 's' to start, 'p' to stop, 't' for stress test\n")

	// input and output files
	in, err := filepath.Abs("./models/three_layer.xml")
	if err != nil {
		log.Fatal(err)
	}
	out, err := filepath.Abs("./out")
	if err != nil {
		log.Fatal(err)
	}

	// Listen for messages
	id := ""
	var s string
	for {
		_, err := fmt.Scan(&s)
		log.Print(s)
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
					ModelPath: in,
					OutDir:    out,
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
				&pb.StopRequest{Uuid: id},
			)
			if err != nil {
				log.Fatal(err)
			}
			log.Printf("response: %v", rp)
		case "t":
			log.Printf("starting stress test with N=%d", STRESS_TEST_N)
			var ids []string
			for i := 0; i < STRESS_TEST_N; i++ {
				rp, err := c.Start(
					ctx,
					&pb.StartRequest{
						ModelPath: in,
						OutDir:    out,
					},
				)
				if err != nil {
          log.Fatalf("[WARNING] err when starting sim: %v", err)
				}
				id = rp.Uuid
				ids = append(ids, id)
			}
			log.Printf("stopping all jobs")
			for _, id := range ids {
				_, err := c.Stop(
					ctx,
					&pb.StopRequest{Uuid: id},
				)
				if err != nil {
          log.Fatalf("[WARNING] err when stopping sim (%s): %v", id, err)
				}
			}
      log.Printf("done")
		default:
			log.Print("type 's' to start, 'p' to stop, 't' for stress test")
		}
	}
}
