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

def udp_forwarder():
    """" check the redis for changes against the local dictionary and if a change
    happens update the DNAT rule"""
    mapps = {}
    # get data from redis instance where the key contains '_' to identify the map
    for key in redis_instance.keys():
        if str(key.decode('utf-8')).contains(')'):
            mapps[str(key.decode('utf-8'))] = redis_instance.get(key)
    print(mapps)

    # check if the values in mapp are the same as in redis




class Command(BaseCommand):
    def handle(self, *args, **options):
        udp_forwarder()