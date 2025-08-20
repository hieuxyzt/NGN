from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel


def createServer(net, serverName):
    server = net.get(serverName);
    server.cmd("nohup java -Xms100m -Xmx100m -jar server.jar > info.log 2>&1&");

def removeServer(net, serverName):
    server = net.get(serverName);
    server.cmd("kill `ps -ef | grep java | grep -v grep | awk '{print$2}'`");

def initContainernet():
    setLogLevel('info')
    net = Containernet(controller=Controller)
    net.addController('c0')

    try:
        info('*** Adding switch \n')
        
        sClient = net.addSwitch('s1')
        sLb = net.addSwitch('s2')
        sGateway = net.addSwitch('s3')
        sServer = net.addSwitch('s4')
        sServerOld = net.addSwitch('s41')
        sEureka = net.addSwitch('s5')

        info('*** Adding server and client container\n')

        eureka = net.addDocker('eureka', ip='10.0.10.1', 
            dcmd="nohup java -Xms100m -Xmx100m -jar eureka_server.jar > info.log 2>&1&", 
            dimage="eureka:latest",
            publish_all_ports= True,
            ports=[8761], port_bindings={8761:8761}
        )

        prometheus = net.addDocker('p', ip='10.0.11.1', 
            dimage="my_prometheus:latest",
            publish_all_ports= True,
            ports=[9090], port_bindings={9090:9090}
        )

        scalingServer = net.addDocker('scaling', ip='10.0.12.1', 
            dcmd="nohup java -Xms100m -Xmx100m -jar scaling_server.jar > info.log 2>&1&", 
            dimage="scaling_server:latest",
        )

        gateway = net.addDocker('gateway', ip='10.0.1.1', 
            dcmd="nohup java -Xms100m -Xmx100m -jar cloud_gateway.jar > info.log 2>&1&", 
            dimage="gateway:latest")
        gateway2 = net.addDocker('gateway2', ip='10.0.1.2', 
            dcmd="nohup java -Xms100m -Xmx100m -jar cloud_gateway.jar > info.log 2>&1&", 
            dimage="gateway:latest")
        gateway3 = net.addDocker('gateway3', ip='10.0.1.3', 
            dcmd="nohup java -Xms100m -Xmx100m -jar cloud_gateway.jar > info.log 2>&1&", 
            dimage="gateway:latest")

        numOfServer = 10;
        for i in range(1, numOfServer + 1):
            server = net.addDocker('server' + str(i), ip='10.0.2.' + str(i), 
                #dcmd="nohup java -jar server.jar > info.log 2>&1&", 
                dimage="server:latest")
            net.addLink(server, sServer)
        
        serverOld = net.addDocker('serverOld', ip='10.0.100.1', 
                #dcmd="nohup java -jar server.jar > info.log 2>&1&", 
                dimage="server_old:latest")
        net.addLink(serverOld, sServerOld)

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

        net.addLink(eureka,sEureka)
        net.addLink(prometheus,sEureka)
        net.addLink(scalingServer, sEureka)
        net.addLink(client,sClient)

        net.addLink(lb,sLb)
        net.addLink(lb_backup,sLb)

        net.addLink(gateway,sGateway)
        net.addLink(gateway2,sGateway)
        net.addLink(gateway3,sGateway)


        net.addLink(sClient, sLb, cls=TCLink, delay='1ms', bw=1)
        net.addLink(sLb, sGateway, cls=TCLink, delay='1ms', bw=1)
        net.addLink(sGateway, sServer, cls=TCLink, delay='1ms', bw=1)
        net.addLink(sEureka, sServer, cls=TCLink, delay='1ms', bw=1)
        net.addLink(sGateway, sServerOld, cls=TCLink, delay='50ms', bw=1)

        net.start()

        info('*** Starting to execute commands\n')
        serverOld.cmd("nohup java -Xms100m -Xmx100m -jar server.jar > info.log 2>&1&")

        info('set up master nginx')
        lb.cmd("service keepalived start -D && nginx")
        info(lb.cmd("nginx -t") + "\n")
        info(lb.cmd("keepalived -t -f /etc/keepalived/keepalived.conf") + "\n")

        info('set up backup nginx')
        lb_backup.cmd("service keepalived start -D && nginx")
        info(lb_backup.cmd("nginx -t") + "\n")
        info(lb_backup.cmd("keepalived -t -f /etc/keepalived/keepalived.conf") + "\n")

        info('set up prometheus')
        prometheus.cmd("nohup ./prometheus --config.file=prometheus.yml > info.log 2>&1&")
        # info('Execute: client.cmd("time curl 10.0.0.1/server")\n')
        # info(client.cmd("time curl -X POST 10.0.0.1/server") + "\n")

    except Exception as e:
        info("Error setup containernet!!!!!\n", e)
    finally:
        return net;
