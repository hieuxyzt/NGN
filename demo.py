#!/usr/bin/python
"""
This is an example how to simulate a client server environment.
"""
from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
import time

setLogLevel('info')

net = Containernet(controller=Controller)
net.addController('c0')

info('*** Adding server and client container\n')
server = net.addDocker('server', ip='10.0.1.1', dcmd="python app.py", dimage="server:latest")
server2 = net.addDocker('server2', ip='10.0.1.2', dcmd="python app.py", dimage="server:latest")
server3 = net.addDocker('server3', ip='10.0.1.3', dcmd="python app.py", dimage="server:latest")

client = net.addDocker('client', ip='10.0.2.1', dimage="client:latest")
lb = net.addDocker(
    'lb', ip='10.0.0.2', dimage="nginx:latest", 
    publish_all_ports= True,
    ports=[80], port_bindings={80:80}
)

lb_backup = net.addDocker(
    'lb_backup', ip='10.0.0.3', dimage="nginx_backup:latest", 
    #publish_all_ports= True,
    #ports=[80], port_bindings={81:80}
)

info('*** Setup network\n')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
s3 = net.addSwitch('s3')

net.addLink(server,s1)
net.addLink(server2,s1)
net.addLink(server3,s1)

net.addLink(lb,s2)
net.addLink(lb_backup,s2)

net.addLink(client,s3)

net.addLink(s1, s2, cls=TCLink, delay='10ms', bw=1)
net.addLink(s2, s3, cls=TCLink, delay='1ms', bw=1)
net.start()

info('*** Starting to execute commands\n')

info('set up master nginx')
lb.cmd("service keepalived start -D && nginx")
info(lb.cmd("nginx -t") + "\n")
info(lb.cmd("keepalived -t -f /etc/keepalived/keepalived.conf") + "\n")

info('set up backup nginx')
lb_backup.cmd("service keepalived start -D && nginx")
info(lb_backup.cmd("nginx -t") + "\n")
info(lb_backup.cmd("keepalived -t -f /etc/keepalived/keepalived.conf") + "\n")

info('Execute: client.cmd("time curl 10.0.0.1")\n')
info(client.cmd("time curl 10.0.0.1") + "\n")

info('Execute: client.cmd("time curl 10.0.0.1/hello/42")\n')
info(client.cmd("time curl 10.0.0.1/hello/42") + "\n")

CLI(net)

net.stop()
