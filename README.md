# evomorph

## Setup

Use [Go](https://go.dev) to install [reflex](https://github.com/cespare/reflex), [protoc-gen-go](https://pkg.go.dev/google.golang.org/protobuf/cmd/protoc-gen-go), and [protoc-gen-go-grpc](https://pkg.go.dev/google.golang.org/grpc/cmd/protoc-gen-go-grpc).

```
go install github.com/cespare/reflex@latest
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

## Build

After updating any protos, rebuild them with `protoc`.

```
protoc *.proto --go_out=go --go-grpc_out=go
```

## Run

You can invoke reflex via the `run` script.

```
./run [component]
```

Where `[component]` is one of `{engine, engine/test, controller}`.
