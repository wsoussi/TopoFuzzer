import subprocess
from django.core.management.base import BaseCommand
import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE','my_django_project.settings')
import django
django.setup()
import time
# from mininet.topolib import TorusTopo, TreeNet, TreeTopo
from mininet.topolib import Topo
from django.conf import settings
import redis
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch, Node
import threading
import asyncio
import socket
from proxy_handler.tcpproxy import tcpproxy
import pickle

from mininet.examples.multipoll import monitorFiles
mn_ipBase = "10.70.0.0/16"


class NAT( Node ):
    "NAT: Provides connectivity to external network"

    def __init__( self, name, subnet=mn_ipBase,
                  localIntf=None, flush=False, **params):
        """Start NAT/forwarding between Mininet and external network
           subnet: Mininet subnet (default 10.0/8)
           flush: flush iptables before installing NAT rules"""
        super( NAT, self ).__init__( name, **params )

        self.subnet = subnet
        self.localIntf = localIntf
        self.flush = flush
        self.forwardState = self.cmd( 'sysctl -n net.ipv4.ip_forward' ).strip()

    def setManualConfig( self, intf ):
        """Prevent network-manager/networkd from messing with our interface
           by specifying manual configuration in /etc/network/interfaces"""
        cfile = '/etc/network/interfaces'
        line = '\niface %s inet manual\n' % intf
        try:
            with open( cfile ) as f:
                config = f.read()
        except IOError:
            config = ''
        if ( line ) not in config:
            info( '*** Adding "' + line.strip() + '" to ' + cfile + '\n' )
            with open( cfile, 'a' ) as f:
                f.write( line )
            # Probably need to restart network manager to be safe -
            # hopefully this won't disconnect you
            self.cmd( 'service network-manager restart || netplan apply' )

    # pylint: disable=arguments-differ
    def config( self, **params ):
        """Configure the NAT and iptables"""

        if not self.localIntf:
            self.localIntf = self.defaultIntf()

        self.setManualConfig( self.localIntf )

        # Now we can configure manually without interference
        super( NAT, self).config( **params )

        if self.flush:
            # self.cmd( 'sysctl net.ipv4.ip_forward=0' )
            self.cmd( 'iptables -F' )
            # self.cmd( 'iptables -t nat -F' )
            # Create default entries for unmatched traffic
            self.cmd( 'iptables -P INPUT ACCEPT' )
            self.cmd( 'iptables -P OUTPUT ACCEPT' )
            self.cmd( 'iptables -P FORWARD DROP' )

        # Install NAT rules
        self.cmd( 'iptables -I FORWARD',
                  '-i', self.localIntf, '-d', self.subnet, '-j DROP' )
        self.cmd( 'iptables -A FORWARD',
                  '-i', self.localIntf, '-s', self.subnet, '-j ACCEPT' )
        self.cmd( 'iptables -A FORWARD',
                  '-o', self.localIntf, '-d', self.subnet, '-j ACCEPT' )
        # self.cmd( 'iptables -t nat -A POSTROUTING',
        #           '-s', self.subnet, "'!'", '-d', self.subnet,
        #           '-j MASQUERADE' )
        # Instruct the kernel to perform forwarding
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )
        # self.cmd('iptables -t nat -D POSTROUTING 1')

    def terminate( self ):
        "Stop NAT/forwarding between Mininet and external network"
        # Remote NAT rules
        self.cmd( 'iptables -D FORWARD',
                   '-i', self.localIntf, '-d', self.subnet, '-j DROP' )
        self.cmd( 'iptables -D FORWARD',
                  '-i', self.localIntf, '-s', self.subnet, '-j ACCEPT' )
        self.cmd( 'iptables -D FORWARD',
                  '-o', self.localIntf, '-d', self.subnet, '-j ACCEPT' )
        # self.cmd( 'iptables -t nat -D POSTROUTING',
        #           '-s', self.subnet, '\'!\'', '-d', self.subnet,
        #           '-j MASQUERADE' )
        # Put the forwarding state back to what it was
        self.cmd( 'sysctl net.ipv4.ip_forward=%s' % self.forwardState )
        super( NAT, self ).terminate()

def addNAT(net, name='nat0', connect=True, inNamespace=False,
           **params):
    """Add a NAT to the Mininet network
       name: name of NAT node
       connect: switch to connect to | True (s1) | None
       inNamespace: create in a network namespace
       params: other NAT node params, notably:
           ip: used as default gateway address"""
    nat = net.addHost(name, cls=NAT, inNamespace=inNamespace,
                       subnet=net.ipBase, **params)
    # find first switch and create link
    if connect:
        if not isinstance(connect, Node):
            # Use first switch if not specified
            connect = net.switches[0]
        # Connect the nat to the switch
        net.addLink(nat, connect)
        # Set the default route on hosts
        natIP = nat.params['ip'].split('/')[0]
        for host in net.hosts:
            if host.inNamespace:
                host.setDefaultRoute('via %s' % natIP)
    return nat


class TreeTopo( Topo ):
    "Topology for a tree network with a given depth and fanout."

    def build( self, depth=1, fanout=2 ):
        # Numbering:  h1..N, s1..M
        self.hostNum = 1
        self.switchNum = 1
        # Build topology
        self.addTree( depth, fanout )

    def addTree( self, depth, fanout ):
        """Add a subtree starting with node n.
           returns: last node added"""
        isSwitch = depth > 0
        if isSwitch:
            node = self.addSwitch( 's%s' % self.switchNum )
            self.switchNum += 1
            for _ in range( fanout ):
                child = self.addTree( depth - 1, fanout )
                self.addLink( node, child )
        else:
            node = self.addHost( 'h%s' % self.hostNum) # ip="10.70.1." + str(self.hostNum), defaultRoute = "via 10.70.0.1"
            self.hostNum += 1
        return node


def TreeNet( depth=1, fanout=2, **kwargs ):
    "Convenience function for creating tree networks."
    topo = TreeTopo( depth, fanout )
    return Mininet( topo, **kwargs )


class Object(object):
    pass

# Connect to our Redis instance
redis_instance = redis.StrictRedis(host=settings.TOPOFUZZER_IP,
                                  port=settings.REDIS_PORT, password= "topofuzzer", db=0, charset='utf-8', decode_responses=True)

mn_hosts_number = 20

threads = []

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        super( LinuxRouter, self ).terminate()


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

# def add_port_s1(net, mn_ip):
#     proxy_port = settings.PROXY_PORT
#     command0 = "sudo iptables -t nat -A PREROUTING -d "+ mn_ip +" -p tcp -m tcp --dport "+ str(settings.PROXY_PORT) +" -j ACCEPT"
#     command1 = "sudo iptables -t nat -A PREROUTING -d "+ mn_ip +" -p tcp -m tcp --dport 1:65535 -j DNAT --to-destination "+ mn_ip +":"+str(proxy_port)
#     s1 = net.get("s1")
#     s1.cmd(command0)
#     s1.cmd(command1)

def add_TPROXY_rule(h, mn_ip, count):
    proxy_port = settings.PROXY_PORT
    command0 = "ip route add local " + mn_ip + " dev lo src 127.0.0." + str(count + 1)
    command1 = "iptables -t mangle -I PREROUTING ! -s 10.161.2.164 -d " + mn_ip + " -p tcp -j TPROXY --on-port=" + str(proxy_port) + " --on-ip=127.0.0." + str(count + 1)
    h.cmd(command0)
    h.cmd(command1)


def start_mininet_with_NAT(onos_ip, onos_sdnc_port):
    # clear whatever is in mininet
    print(os.system("sudo mn -c"))
    # topo = TorusTopo(3,3,1)
    controller = RemoteController('c0', ip=onos_ip, port=onos_sdnc_port, protocols="OpenFlow13")

    net = TreeNet(depth=1, fanout=mn_hosts_number, controller=controller, ipBase=mn_ipBase)
    # net = Mininet(topo=topo, controller=controller, ipBase='111.0.0.0/8') #topo=topo
    # net.addController(controller)

    # add customized NAT
    addNAT(net).configDefault()

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
            add_TPROXY_rule(h, h.IP(), count)
            h.cmd("setcap cap_net_raw,cap_net_admin=eip manage.py")
            h.cmd("setcap cap_net_raw,cap_net_admin=eip mnHostProxy.py")
            # start the tcp proxy script and make it look first for the privateIP in redis, if no privateIP is found, the script will sleep and check every 1 second
            h.cmd('python manage.py mnHostProxy --proxy-ip ' + h.IP() + ' &> tcp_outputfile' + h.IP() + ' &')
            # start the udp proxy script in the same way
            h.cmd('python manage.py udp_nat --proxy-ip ' + h.IP() + ' &> udp_outputfile' + h.IP() + ' &')
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