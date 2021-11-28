from concurrent import futures
import grpc
import Simulation_pb2_grpc
import Simulation_pb2
from converter import converter

class SimulatorServicer(Simulation_pb2_grpc.SimulatorServicer):

    def RunSimulation(self, request, context):
        print("Received")
        print(request)

        response = converter(request)

        #response = "server"
        return Simulation_pb2.SimResponse(message=response)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Simulation_pb2_grpc.add_SimulatorServicer_to_server(
        SimulatorServicer(), server)
    server.add_insecure_port('[::]:9090')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()