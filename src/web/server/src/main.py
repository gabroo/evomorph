from flask import Flask, request
import grpc

from protos import sim_pb2
from protos import sim_pb2_grpc
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET", "POST"])
def welcome():
    if request.method == "POST":
        data = request.get_json()
        if data is None:
            return "request JSON returned None"

        query = data["simulationTitle"]

        with grpc.insecure_channel("localhost:9090") as channel:
            stub = sim_pb2_grpc.SimulatorStub(channel)
            q = sim_pb2.Simulation(
                numACells=int(data["numACells"]),
                numBCells=int(data["numBCells"]),
                gammaA=float(data["gammaA"]),
                gammaB=float(data["gammaB"]),
                xValue=int(data["xValue"]),
                yValue=int(data["yValue"]),
                zValue=int(data["zValue"]),
                stopTime=int(data["stopTime"]),
            )
            response = stub.RunSimulation(q)
            if response:
                print(response.message)
                path = "/results/" + data["simulationTitle"] + ".xml"
                filename = ".." + path
                responsename = "web" + path

                f = open(filename, "w")
                f.write(response.message)
                f.close()

                return responsename
        print(query)


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
