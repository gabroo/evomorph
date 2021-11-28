from flask import Flask, request
import grpc
# import echo_pb2
# import echo_pb2_grpc
import Simulation_pb2
import Simulation_pb2_grpc
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def welcome():
    #print("gotMessage")
    #print(request.method)
    #query = "hello"
    if request.method == 'POST':
        #print('hi')
        data = request.get_json()
        #print(data)
        query = data['simulationTitle']

        with grpc.insecure_channel('localhost:9090') as channel:
            stub = Simulation_pb2_grpc.SimulatorStub(channel)
            q = Simulation_pb2.Simulation(numACells=int(data['numACells']), numBCells=int(data['numBCells']), gammaA=float(data['gammaA']), gammaB=float(data['gammaB']), 
                xValue=int(data['xValue']), yValue=int(data['yValue']), zValue=int(data['zValue']), stopTime=int(data['stopTime']))
            response = stub.RunSimulation(q)
            if response:
                print(response.message)
                path = '/results/' + data['simulationTitle'] + '.xml'
                filename = '..' + path
                responsename = 'web' + path
                
                f = open(filename, "w")
                f.write(response.message)
                f.close()
                
                return (responsename)
    print(query)
    # with grpc.insecure_channel('localhost:9090') as channel:
    #     stub = echo_pb2_grpc.EchoServiceStub(channel)
    #     q = echo_pb2.EchoRequest(message=query)
    #     response = stub.Echo(q)
    #     if response:
    #         print(response.message)
    #         return (query + ' ' + response.message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)