#!/usr/bin/python
"""
This is an example how to simulate a client server environment.
"""
from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel

setLogLevel('info')

net = Containernet(controller=Controller)
net.addController('c0')

info('*** Adding server and client container\n')
server = net.addDocker('server', ip='10.0.1.1', dcmd="python app.py", dimage="server:latest")
client = net.addDocker('client', ip='10.0.2.1', dimage="client:latest")
lb = net.addDocker(
    'lb', ip='10.0.0.1', dimage="nginx:latest", 
    publish_all_ports= True,
    ports=[80], port_bindings={80:80}
)


info('*** Setup network\n')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
s3 = net.addSwitch('s3')

net.addLink(server,s1)
net.addLink(lb,s2)
net.addLink(client,s3)

net.addLink(s1, s2, cls=TCLink, delay='10ms', bw=1)
net.addLink(s2, s3, cls=TCLink, delay='1ms', bw=1)
net.start()

info('*** Starting to execute commands\n')
info('Start nginx\n')
info(lb.cmd("nginx"))

info('Execute: client.cmd("time curl 10.0.0.1")\n')
info(client.cmd("time curl 10.0.0.1") + "\n")

info('Execute: client.cmd("time curl 10.0.0.1/hello/42")\n')
info(client.cmd("time curl 10.0.0.1/hello/42") + "\n")

CLI(net)

net.stop()
