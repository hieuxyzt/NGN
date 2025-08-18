from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel


def createServer(net, serverName, serverIp):
    server = net.addDocker(serverName, ip=serverIp, dcmd="python app.py", dimage="server:latest")
    return server

def stopHost(net, hostName):
    host = net.get(hostName)
    host.terminate()
    net.hosts.remove(host)

def initContainernet():
    setLogLevel('info')
    net = Containernet(controller=Controller)
    net.addController('c0')

    info('*** Adding server and client container\n')

    eureka = net.addDocker('eureka', ip='10.0.10.1', 
        dcmd="nohup java -jar eureka_server.jar > info.log 2>&1&", 
        dimage="eureka:latest",
        publish_all_ports= True,
        ports=[8761], port_bindings={8761:8761}
    )

    gateway = net.addDocker('gateway', ip='10.0.1.1', 
        dcmd="nohup java -jar cloud_gateway.jar > info.log 2>&1&", 
        dimage="gateway:latest")
    gateway2 = net.addDocker('gateway2', ip='10.0.1.2', 
        dcmd="nohup java -jar cloud_gateway.jar > info.log 2>&1&", 
        dimage="gateway:latest")
    gateway3 = net.addDocker('gateway3', ip='10.0.1.3', 
        dcmd="nohup java -jar cloud_gateway.jar > info.log 2>&1&", 
        dimage="gateway:latest")

    server = net.addDocker('server', ip='10.0.2.1', 
        dcmd="nohup java -jar server.jar > info.log 2>&1&", 
        dimage="server:latest")
    server2 = net.addDocker('server2', ip='10.0.2.2',
        dcmd="nohup java -jar server.jar > info.log 2>&1&", 
        dimage="server:latest")
    server3 = net.addDocker('server3', ip='10.0.2.3', 
        dcmd="nohup java -jar server.jar > info.log 2>&1&", 
        dimage="server:latest")

    client = net.addDocker('client', ip='10.0.20.1', dimage="client:latest")
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
    sClient = net.addSwitch('sClient0')
    sLb = net.addSwitch('sLb0')
    sGateway = net.addSwitch('sGateway0')
    sServer = net.addSwitch('sServer0')
    sEureka = net.addSwitch('sEureka0')

    net.addLink(eureka,sEureka)
    net.addLink(client,sClient)

    net.addLink(lb,sLb)
    net.addLink(lb_backup,sLb)

    net.addLink(gateway,sGateway)
    net.addLink(gateway2,sGateway)
    net.addLink(gateway3,sGateway)

    net.addLink(server,sServer)
    net.addLink(server2,sServer)
    net.addLink(server3,sServer)

    net.addLink(sClient, sLb, cls=TCLink, delay='10ms', bw=1)
    net.addLink(sLb, sGateway, cls=TCLink, delay='1ms', bw=1)
    net.addLink(sGateway, sServer, cls=TCLink, delay='1ms', bw=1)
    net.addLink(sGateway, sServer, cls=TCLink, delay='1ms', bw=1)
    net.addLink(sEureka, sLb, cls=TCLink, delay='1ms', bw=1)

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

    return net;

