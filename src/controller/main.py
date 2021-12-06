import grpc

import protos.engine_pb2 as engine
import protos.engine_pb2_grpc as engine_grpc


def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = engine_grpc.EngineStub(channel)
    req = engine.StartRequest(model_path="in", out_dir="out")
    rep = stub.Start(req)
    print(f"status: {rep.status}\nid: {rep.id}")


if __name__ == "__main__":
    run()
