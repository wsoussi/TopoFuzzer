import subprocess
from django.core.management.base import BaseCommand
import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE','my_django_project.settings')
import django
django.setup()
import time
from mininet.topolib import TorusTopo, TreeNet
from django.conf import settings
import redis
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
import threading
import socket
from proxy_handler.tcpproxy import tcpproxy
import pickle

from mininet.examples.multipoll import monitorFiles

class Object(object):
    pass

# Connect to our Redis instance
redis_instance = redis.StrictRedis(host=settings.TOPOFUZZER_IP,
                                  port=settings.REDIS_PORT, password= "topofuzzer", db=0, charset='utf-8', decode_responses=True)

mn_hosts_number = 20

mn_ipBase = "10.70.0.0/16"

threads = []


# implement "killable" thread
class thread_with_trace(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False
        self.handled = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True
        self.handled = True


# def createTopo(net, nb_hosts):
#     s1 = net.addSwitch('s1', cls = OVSKernelSwitch, protocols = 'OpenFlow13')
#     for i in range(1,nb_hosts + 1):
#         h = net.addHost("h"+str(i))
#         net.addLink(s1, h)


def add_port_nat(net, mn_ip):
    proxy_port = settings.PROXY_PORT
    command0 = "sudo iptables -t nat -A PREROUTING -d "+ mn_ip +" -p tcp -m tcp --dport "+ str(settings.PROXY_PORT) +" -j ACCEPT"
    command1 = "sudo iptables -t nat -A PREROUTING -d "+ mn_ip +" -p tcp -m tcp --dport 1:65535 -j DNAT --to-destination "+ mn_ip +":"+str(proxy_port)
    nat0 = net.get("nat0")
    nat0.cmd(command0)
    nat0.cmd(command1)


def start_mininet_with_NAT(onos_ip, onos_sdnc_port):
    # clear whatever is in mininet
    print(os.system("sudo mn -c"))
    # topo = TorusTopo(3,3,1)
    controller = RemoteController('c0', ip=onos_ip, port=onos_sdnc_port, protocols="OpenFlow13")

    net = TreeNet(depth=1, fanout=mn_hosts_number, controller=controller, ipBase=mn_ipBase)
    # net = Mininet(topo=topo, controller=controller, ipBase='111.0.0.0/8') #topo=topo
    # net.addController(controller)

    net.addNAT().configDefault()
    net.start()

    # check every VNF and assign a host through redis
    # this is done in views.py throught API calls
    redis_instance.set("total_mn_hosts", mn_hosts_number)
    redis_instance.set("free_mn_hosts", mn_hosts_number)

    # go to the proxy script in each host
    hosts = net.hosts
    count = 0
    for h in hosts:
        if count < 4:
            h.cmd('cd pycharmh1_project/TopoFuzzer | ls')
            # add NAT rule to nat0 node to redirect ports to port 5555 of the specific host ip
            add_port_nat(net, h.IP())
            # start the proxy script and make it look first for the privateIP in redis, if no privateIP is found, the script will sleep and check every 1 second
            h.cmd('python manage.py mnHostProxy --proxy-ip ' + h.IP() + ' &> outputfile' + h.IP() + ' &')
            print("done" + str(count))
        count += 1
    CLI(net)
    net.stop()


def log(handle, message, message_only=False):
    # if message_only is True, only the message will be logged
    # otherwise the message will be prefixed with a timestamp and a line is
    # written after the message to make the log file easier to read
    if not isinstance(message, bytes):
        message = bytes(message, 'ascii')
    if handle is None:
        return
    if not message_only:
        logentry = bytes("%s %s\n" % (time.strftime('%Y%m%d-%H%M%S'), str(time.time())), 'ascii')
    else:
        logentry = b''
    logentry += message
    if not message_only:
        logentry += b'\n' + b'-' * 20 + b'\n'
    handle.write(logentry)


def manage_proxies(motdec_ip, onos_port):
    global threads
    # start mininet topology
    start_mininet_with_NAT(motdec_ip, onos_port)


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--onos-ip', dest='onos_ip', type=str, help='MOTDEC hostname or IP address', action="store", required=True)

        # Named (optional) arguments
        parser.add_argument('--onos-port', type=int, help='ONOS port', required=False)

    def handle(self, *args, **options):
        if options['onos_port']:
            onos_port = options['onos_port']
        else:
            onos_port = 6653
        onos_ip = options['onos_ip']
        manage_proxies(onos_ip, onos_port)