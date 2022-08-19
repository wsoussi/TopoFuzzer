from django.core.management.base import BaseCommand
import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE','my_django_project.settings')
import django
django.setup()
from mininet.topolib import TorusTopo
from django.conf import settings
import redis
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController
import threading
import socket
from proxy_handler.tcpproxy import tcpproxy

class Object(object):
    pass

# Connect to our Redis instance
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0, charset='utf-8', decode_responses=True)

HOST = "10.161.1.135"  # Proxy Standard loopback interface address (localhost)
PORT = 5555  # Proxy Port to listen on

ip_mapping = {"10.161.1.135": "10.161.1.140"}
port_mapping = {5555: 8080}

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


def start_mininet_with_NAT(onos_ip, onos_sdnc_port):
    topo = TorusTopo(3,3,1)

    controller = RemoteController('c0', ip=onos_ip, port=onos_sdnc_port, protocols="OpenFlow13")

    net = Mininet(topo=topo, controller=None, ipBase='11.0.0.0/8')
    net.addController(controller)
    net.addNAT().configDefault()

    net.start()
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
def manage_proxies(motdec_port, onos_port):
    global threads
    #TODO LATER  start mininet topology
    #start_mininet_with_NAT(motdec_ip, onos_port)

    # TODO LATER enter one of mininet hosts

    # TODO start proxy
    args = Object()
    args.verbose = True
    args.use_ssl = False
    args.client_certificate = None
    args.client_key = None
    args.server_certificate = None
    args.server_key = None
    args.proxy_ip = None
    args.proxy_port = None
    args.proxy_type = 'SOCKS5'
    args.in_modules = None
    args.out_modules = None
    args.no_chain_modules = False
    args.logfile = None
    args.list = None
    args.help_modules = None
    args.listen_ip = HOST
    args.listen_port = PORT
    args.target_ip = redis_instance.get(args.listen_ip.replace(".", "-"))
    args.target_port = port_mapping[args.listen_port]

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

    if args.list:
        list_modules()
        sys.exit(0)

    if args.help_modules is not None:
        print_module_help(args.help_modules)
        sys.exit(0)

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
        in_modules = generate_module_list(args.in_modules, incoming=True, verbose=args.verbose)
    else:
        in_modules = None

    if args.out_modules is not None:
        out_modules = generate_module_list(args.out_modules, incoming=False, verbose=args.verbose)
    else:
        out_modules = None

    # this is the socket we will listen on for incoming connections
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        proxy_socket.bind((args.listen_ip, args.listen_port))
    except socket.error as e:
        print(e.strerror)
        sys.exit(5)

    proxy_socket.listen(100)
    # endless loop until ctrl+c
    try:
        while True:
            in_socket, in_addrinfo = proxy_socket.accept()
            print('Connection from %s:%d' % in_addrinfo)
            # create thread if the in_socket is
            proxy_thread = thread_with_trace(target=tcpproxy.start_proxy_thread,
                                             args=(in_socket, args, in_modules,
                                                   out_modules))
            print("Starting proxy thread " + proxy_thread.name)
            proxy_thread.start()
            # thread_dict = {"p_thread": proxy_thread, "in_socket" : in_socket, "args": args}
            # threads.append(thread_dict)
            # # print("the thread list is " + str(threads))
            # # if server IP changed replace the socket thread with a new one
            # new_threads = []
            # for thread_dict in threads:
            #     p_thread = thread_dict["p_thread"]
            #     thread_in_socket = thread_dict["in_socket"]
            #     thread_args = thread_dict["args"]
            #     actual_target_ip = redis_instance.get(thread_args.listen_ip.replace(".", "-"))
            #     # TODO include actual_target_ip in the thread tuple
            #     # mark old closed threads
            #     if not p_thread.is_alive():
            #         p_thread.handled = True
            #     # if thread alive and target_ip changes kill the thread with old out_socket and start one with a new out_socket
            #     if not p_thread.handled and actual_target_ip != thread_args.target_ip:
            #         print("\nA change happened, the new ip is " + actual_target_ip)
            #         p_thread.kill()
            #         p_thread.handled = True
            #         thread_args.target_ip = actual_target_ip
            #         proxy_thread = thread_with_trace(target=tcpproxy.start_proxy_thread,
            #                                          args=(thread_in_socket, thread_args, in_modules,
            #                                                out_modules))
            #         proxy_thread.start()
            #         new_thread_dict = {"p_thread": proxy_thread, "in_socket": thread_in_socket, "args": thread_args}
            #         new_threads.append(new_thread_dict)
            # threads = threads + new_threads
            # threads = [thread_dict for thread_dict in threads if not thread_dict["p_thread"].handled]

    except KeyboardInterrupt:
        log(args.logfile, 'Ctrl+C detected, exiting...')
        print('\nCtrl+C detected, exiting...')
        sys.exit(0)




class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--motdec-ip', dest='motdec_ip', type=str, help='MOTDEC hostname or IP address', action="store", required=True)

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
            onos_port = 8181
        motdec_ip = options['motdec_ip']
        manage_proxies(motdec_ip, onos_port)


