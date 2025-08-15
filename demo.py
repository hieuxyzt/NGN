#!/usr/bin/python

from mininet.log import info, setLogLevel
from mininet.cli import CLI

import time
from flask import Flask, request, jsonify
import containernet_service as containernetService

setLogLevel('info')
app = Flask(__name__)

net = containernetService.initContainernet()

@app.route("/createServer", methods=['POST'])
def createServer():
    data = request.get_json()
    info("Clear request create server: ", data, "\n")
    containernetService.createServer(net, data["name"], data["ip"])
    return "ok"

@app.route("/stopHost", methods=['POST'])
def stopHost():
    data = request.get_json()
    info("Clear request stop host: ", data, "\n")
    containernetService.stopHost(data["name"])
    return "ok"

@app.route("/addLink", methods=['POST'])
def addLink():
    data = request.get_json()
    info("Clear request add link: ", data, "\n")
    net.addLink(data["host"], data["switch"])
    return "ok"

@app.route("/updateNginx", methods=['POST'])
def updateNginx():
    return "ok"


if __name__ == "__main__":
    # CLI(net)
    app.run(host='0.0.0.0', port=1234)
    net.stop()
