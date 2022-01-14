package gateway

import (
	"context"
	"log"
	"mime"
	"time"

	"crypto/tls"
	"io/fs"
	"net/http"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	gwrt "github.com/grpc-ecosystem/grpc-gateway/v2/runtime"

	"github.com/gabroo/evomorph/protos/docs"
	pb "github.com/gabroo/evomorph/protos/go"
)

var (
	GW_ADDR   = "0.0.0.0:8081"
	GRPC_ADDR = "0.0.0.0:50052"
	CERT_DUR  = 90 * 24 * time.Hour
)

// getOpenAPIHandler serves an OpenAPI UI.
// Adapted from https://github.com/philips/grpc-gateway-example/blob/a269bcb5931ca92be0ceae6130ac27ae89582ecc/cmd/serve.go#L63
func getOpenAPIHandler() http.Handler {
	mime.AddExtensionType(".svg", "image/svg+xml")
	// Use subdirectory in embedded files
	subFS, err := fs.Sub(docs.OpenAPI, "OpenAPI")
	if err != nil {
		panic("couldn't create sub filesystem: " + err.Error())
	}
	return http.FileServer(http.FS(subFS))
}

func getTLSConfig(dur time.Duration) *tls.Config {
	if err := genCert(dur); err != nil {
		log.Fatal(err)
	}

	cert, err := tls.LoadX509KeyPair("cert.pem", "key.pem")
	if err != nil {
		log.Fatal(err)
	}

	config := &tls.Config{
		Certificates:             []tls.Certificate{cert},
		CipherSuites:             nil,
		PreferServerCipherSuites: true,
		MinVersion:               tls.VersionTLS13,
		CurvePreferences: []tls.CurveID{
			tls.CurveP256,
			tls.X25519,
		},
	}
	return config
}

func Run(ctx context.Context) error {
	config := getTLSConfig(CERT_DUR)
	conn, err := grpc.DialContext(
		ctx,
		GRPC_ADDR,
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		return err
	}

	go func() {
		<-ctx.Done()
		if err := conn.Close(); err != nil {
			log.Fatalf("failed to close a client connection to gRPC server: %v", err)
		}
	}()

	gw := gwrt.NewServeMux()
	if err := pb.RegisterControllerHandler(ctx, gw, conn); err != nil {
		return err
	}

	mux := http.NewServeMux()
	mux.Handle("/", gw)
	mux.Handle("/docs/", http.StripPrefix("/docs/", getOpenAPIHandler()))
	mux.HandleFunc("/healthz/", healthzServer(conn))

	s := &http.Server{
		Addr:         GW_ADDR,
		Handler:      allowCORS(mux),
		TLSConfig:    config,
		TLSNextProto: map[string]func(*http.Server, *tls.Conn, http.Handler){},
	}

	go func() {
		<-ctx.Done()
		log.Printf("shutting down gateway")
		if err := s.Shutdown(context.Background()); err != nil {
			log.Fatalf("failed to shut down gateway: %v", err)
		}
	}()

	log.Printf("starting gateway at %s", GW_ADDR)
	if err := s.ListenAndServe(); err != http.ErrServerClosed {
		log.Fatalf("failed to start gateway: %v", err)
	}
	return nil
}
