import subprocess

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/start")
def start_simulation():
    d = request.json
    print(d)
    r = subprocess.run(["morpheus"])
    return jsonify(["simulation started", r])
