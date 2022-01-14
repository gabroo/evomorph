package main

import (
	"context"
	"log"
	"os"

	"crypto/tls"
	"crypto/x509"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"

	pb "github.com/gabroo/evomorph/protos/go"
)

const (
	ADDR = "0.0.0.0:50052"
	BASE = "./"
)

// loadTLSCfg will load a certificate and create a tls config
func loadTLSCfg() *tls.Config {
	b, _ := os.ReadFile("cert/server.crt")
	cp := x509.NewCertPool()
	if !cp.AppendCertsFromPEM(b) {
		log.Fatal("credentials: failed to append certificates")
	}
	config := &tls.Config{
		InsecureSkipVerify: false,
		RootCAs:            cp,
	}
	return config
}

func main() {
	ctx := context.Background()
	// Load our TLS certificate and use grpc/credentials to create new transport credentials
	creds := credentials.NewTLS(loadTLSCfg())
	// Create a new connection using the transport credentials
	conn, err := grpc.DialContext(ctx, ADDR, grpc.WithTransportCredentials(creds))

	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()
	// A new GRPC client to use
	client := pb.NewControllerClient(conn)
	rq := &pb.RunRequest{
		Name:   "simulation001",
		EndMcs: 24,
		Params: &pb.Params{NumCells: 256},
	}
	rp, err := client.Run(ctx, rq)
	if err != nil {
		log.Fatal(err)
	}
	log.Println(rp)
}
