from django.core.management.base import BaseCommand
import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE','my_django_project.settings')
import django
django.setup()
import time
from mininet.topolib import TorusTopo
from django.conf import settings
import redis
import json
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
import threading
import socket
from proxy_handler.tcpproxy import tcpproxy
import requests

threads = []

# Connect to our Rs1 routeedis instance
redis_instance = redis.StrictRedis(host=settings.TOPOFUZZER_IP,
                                  port=settings.REDIS_PORT, password= "topofuzzer", db=0, charset='utf-8', decode_responses=True)


class Object(object):
    pass

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


def get_target_port_from_conntrack(src_ip, dst_ip, src_port):
    url = "http://"+ settings.TOPOFUZZER_IP +":8000/api/conntrack/"
    payload = json.dumps({
        "dst_ip": dst_ip,
        "src_ip": src_ip,
        "src_port": src_port
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("PUT", url, headers=headers, data=payload)
    res = json.loads(response.text)
    return res["msg"]


def start_proxy(mn_ip, mn_port, vnf_ip):
    args = Object()
    args.verbose = True
    args.use_ssl = False
    args.client_certificate = None
    args.client_key = None
    args.server_certificate = None
    args.server_key = None
    args.proxy_ip = None # mn_ip
    args.proxy_port = None # settings.PROXY_PORT + 1
    args.proxy_type = 'SOCKS5'
    args.in_modules = None
    args.out_modules = None
    args.no_chain_modules = False
    args.logfile = None
    args.list = None
    args.help_modules = None
    args.listen_ip = mn_ip
    args.listen_port = mn_port
    args.target_ip = vnf_ip
    args.target_port = None # filled later

    if ((args.client_key is None) ^ (args.client_certificate is None)):
        print("You must either specify both the client certificate and client key or leave both empty")
        sys.exit(8)

    if args.logfile is not None:
        try:
            args.logfile = open(args.logfile, 'ab', 0)  # unbuffered
        except Exception as ex:
            print('Error opening logfile')
            print(ex)
            sys.exit(4)

    if args.listen_ip != '0.0.0.0' and not tcpproxy.is_valid_ip4(args.listen_ip):
        try:
            ip = socket.gethostbyname(args.listen_ip)
        except socket.gaierror:
            ip = False
        if ip is False:
            print('%s is not a valid IP address or host name' % args.listen_ip)
            sys.exit(1)
        else:
            args.listen_ip = ip

    if args.in_modules is not None:
        in_modules = []
    else:
        in_modules = None

    if args.out_modules is not None:
        out_modules = []
    else:
        out_modules = None

    # this is the socket we will listen on for incoming connections
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    try:
        proxy_socket.bind((args.listen_ip, args.listen_port))
    except socket.error as e:
        print("Error at bind: " + e.strerror)
        sys.exit(5)

    proxy_socket.listen(5)
    # endless loop until ctrl+c
    try:
        while True:
            in_socket, in_addrinfo = proxy_socket.accept()
            print('Connection from %s:%d' % in_addrinfo)
            print("targetting " + args.target_ip + ":" + str(args.target_port))
            # get original port from the TopoFuzzer conntrack
            dst_port = get_target_port_from_conntrack(dst_ip=mn_ip, src_ip=in_addrinfo[0], src_port=in_addrinfo[1])
            args.target_port = int(dst_port)
            # create thread if the in_socket is
            proxy_thread = thread_with_trace(target=tcpproxy.start_proxy_thread,
                                             args=(in_socket, args, in_modules,
                                                   out_modules))
            print("Starting proxy thread " + proxy_thread.name)
            proxy_thread.start()

    except KeyboardInterrupt:
        print('\nCtrl+C detected, exiting...')
        sys.exit(0)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--proxy-ip', dest='proxy_ip', type=str, help='Private IP address of the VNF', action="store", required=True)

        # Named (optional) arguments
        parser.add_argument('--motdec-port', type=str, help='MOTDEC port', action="store", required=False)
        parser.add_argument('--onos-port', type=int, help='ONOS port', required=False)

    def handle(self, *args, **options):
        if options['motdec_port']:
            motdec_port = options['motdec_port']
        else:
            motdec_port = 8000
        if options['onos_port']:
            onos_port = options['onos_port']
        else:
            onos_port = 6653
        mn_ip = options['proxy_ip']
        # idle until a VNF IP is mapped to the proxy
        map_found = False
        while not map_found:
            vnf_ip = redis_instance.get(mn_ip.replace(".", "_"))
            if vnf_ip:
                map_found = True
                print(mn_ip + " found its VNF ip: " + vnf_ip)
            else:
                time.sleep(0.1)
        print("vnf ip: " + vnf_ip)
        start_proxy(mn_ip, settings.PROXY_PORT, vnf_ip)