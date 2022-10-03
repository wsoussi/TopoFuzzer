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

# Connect to our Rs1 routeedis instance
redis_instance = redis.StrictRedis(host=settings.TOPOFUZZER_IP,
                                  port=settings.REDIS_PORT, password= "topofuzzer", db=0, charset='utf-8', decode_responses=True)


def udp_forwarder(mn_ip, vnf_ip):
    # add NAT rule
    print("add NAT rule")
    os.system("sudo iptables -t nat -A PREROUTING -p UDP -d " + mn_ip + " --dport 1:65535 -j DNAT --to-destination " +
              vnf_ip)

    """" check the redis for changes and if a change
    happens update the DNAT rule"""

    # continuously check if new elements are added to the redis instance
    try:
        while True:
            new_vnf_ip = redis_instance.get(mn_ip.replace(".", "_"))
            if new_vnf_ip != vnf_ip:
                print("new vnf ip: " + str(new_vnf_ip))
                # update NAT by removing the old DNAT rule and adding the new one
                os.system("sudo iptables -t nat -D PREROUTING -p UDP -d " + mn_ip + " --dport 1:65535 -j DNAT --to-destination " + vnf_ip)
                os.system("sudo iptables -t nat -A PREROUTING -p UDP -d " + mn_ip + " --dport 1:65535 -j DNAT --to-destination " + new_vnf_ip)
                vnf_ip = new_vnf_ip
            time.sleep(0.0001)
    # if the code is stopped with Ctrl+C delete the DNAT rules for each mapps element
    # and exit the program
    except KeyboardInterrupt:
        print("Exiting program")
        print("Delete DNAT rule")
        os.system("sudo iptables -t nat -D PREROUTING -p udp -d " + mn_ip + " --dport 1:65535 -j DNAT --to-destination " + vnf_ip)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--proxy-ip', dest='proxy_ip', type=str, help='Private IP address of the VNF', action="store", required=True)

    def handle(self, *args, **options):
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
        # add POSTROUTING MASQUERADE rule
        print("add POSTROUTING MASQUERADE rule")
        os.system("sudo iptables -t nat -A POSTROUTING -p UDP -j MASQUERADE")
        # start udp forwarder
        udp_forwarder(mn_ip, vnf_ip)