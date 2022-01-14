package gateway

import (
	"errors"
	"log"
	"os"
	"time"

	"encoding/pem"
	"math/big"

	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"crypto/x509"
	"crypto/x509/pkix"
)

func certTemplate(dur time.Duration) (*x509.Certificate, error) {
	serialNumberLimit := new(big.Int).Lsh(big.NewInt(1), 128)
	serialNumber, err := rand.Int(rand.Reader, serialNumberLimit)
	if err != nil {
		return nil, err
	}

	template := x509.Certificate{
		SerialNumber: serialNumber,
		Subject: pkix.Name{
			Organization: []string{"Google"},
		},
		DNSNames:  []string{"localhost"},
		NotBefore: time.Now(),
		NotAfter:  time.Now().Add(dur),

		KeyUsage:              x509.KeyUsageDigitalSignature,
		ExtKeyUsage:           []x509.ExtKeyUsage{x509.ExtKeyUsageServerAuth},
		BasicConstraintsValid: true,
	}
	return &template, nil
}

func genCert(dur time.Duration) error {
	// elliptic.P256 is the only curve type implemented in assembly
	pvKey, err := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	if err != nil {
		return err
	}

	template, err := certTemplate(dur)
	if err != nil {
		return err
	}
	derBytes, err := x509.CreateCertificate(
		rand.Reader,
		template,
		template,
		&pvKey.PublicKey,
		pvKey,
	)
	if err != nil {
		return err
	}

	// write cert file
	pemCert := pem.EncodeToMemory(&pem.Block{Type: "CERTIFICATE", Bytes: derBytes})
	if pemCert == nil {
		return errors.New("failed to encode certificate to PEM")
	}
	if err := os.WriteFile("cert.pem", pemCert, 0644); err != nil {
		return err
	}
	log.Println("wrote cert.pem")

	// write key file
	pvBytes, err := x509.MarshalPKCS8PrivateKey(pvKey)
	if err != nil {
		return err
	}
	pemKey := pem.EncodeToMemory(&pem.Block{Type: "PRIVATE KEY", Bytes: pvBytes})
	if pemKey == nil {
		return errors.New("failed to encode key to PEM")
	}
	if err := os.WriteFile("key.pem", pemKey, 0600); err != nil {
		return err
	}
	log.Println("wrote key.pem")

	return nil
}
