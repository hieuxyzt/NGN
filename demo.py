#!/usr/bin/python

from mininet.log import info, setLogLevel
from mininet.cli import CLI

import time
from flask import Flask
import containernet_service as containernetService

setLogLevel('info')
app = Flask(__name__)

data = containernetService.initContainernet()

if __name__ == "__main__":
    net = data["net"]
    CLI(net)
    net.stop()
    app.run(host='0.0.0.0', port=1234)
