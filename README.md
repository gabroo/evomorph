# evomorph

## Setup

Install [Go](https://go.dev), [`protoc`](https://grpc.io/docs/protoc-installation), and the following packages.

```
go install github.com/cespare/reflex@latest
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
go install github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-openapiv2@latest
go install github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-grpc-gateway@latest
```

## Build

After updating any protos, rebuild them with the `build` script. OpenAPI docs will be generated automatically.

## Run

You can invoke reflex via the `run` script.

```
./run [component]
```

Where `[component]` is one of `{engine, controller}`.

If you are running `controller`, the OpenAPI reference for the HTTP gateway will be available at `/docs`.

Run the frontend with `yarn`.

```
cd studio
yarn
yarn dev
```
