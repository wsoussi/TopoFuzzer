import subprocess, re
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from proxy_handler.serializers import UserSerializer, GroupSerializer
from proxy_handler.management.commands.mnHostProxy import start_proxy
import json
from django.conf import settings
import redis
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import pickle
from mininet.net import Mininet


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

# Connect to Redis instance
redis_instance = redis.StrictRedis(host=settings.TOPOFUZZER_IP,
                                  port=settings.REDIS_PORT, password= "topofuzzer", db=0, charset='utf-8', decode_responses=True)

@api_view(['GET', 'POST'])
def manage_mappings(request, *args, **kwargs):
    if request.method == 'GET':
        items = {}
        count = 0
        for key in redis_instance.keys("*"):
            if key == "mapped_vnfs":
                for i in range(0, redis_instance.llen(key)):
                    items[str(key) + " " + str(i)] = redis_instance.lindex(key, i)
            else:
                items[key] = redis_instance.get(key)
            count += 1
        response = {
            'count': count,
            'msg': f"Found {count} items.",
            'items': items
        }
        return Response(response, status=200)
    elif request.method == 'POST':
        item = json.loads(request.body)
        key = list(item.keys())[0]
        value = item[key]
        redis_instance.set(key, value)
        response = {
            'msg': f"{key} successfully set to {value}"
        }
        return Response(response, 201)

@api_view(['GET', 'PUT', 'DELETE'])
def manage_mapping(request, *args, **kwargs):
    if request.method == 'GET':
        if kwargs['key']:
            value = redis_instance.get(kwargs['key'])
            if value:
                response = {
                    'key': kwargs['key'],
                    'value': value,
                    'msg': 'success'
                }
                return Response(response, status=200)
            else:
                response = {
                    'key': kwargs['key'],
                    'value': None,
                    'msg': 'Not found'
                }
                return Response(response, status=404)
    elif request.method == 'PUT':
        if kwargs['key']:
            request_data = json.loads(request.body)
            new_value = request_data['new_ip']
            print("new ip is " + str(new_value))
            value = redis_instance.get(kwargs['key'])
            if value:
                redis_instance.set(kwargs['key'], new_value)
                response = {
                    'key': kwargs['key'],
                    'value': value,
                    'msg': f"Successfully updated {kwargs['key']}"
                }
                return Response(response, status=200)
            else:
                response = {
                    'key': kwargs['key'],
                    'value': None,
                    'msg': 'Not found'
                }
                return Response(response, status=404)

    elif request.method == 'DELETE':
        if kwargs['key']:
            result = redis_instance.delete(kwargs['key'])
            if result == 1:
                response = {
                    'msg': f"{kwargs['key']} successfully deleted"
                }
                return Response(response, status=404)
            else:
                response = {
                    'key': kwargs['key'],
                    'value': None,
                    'msg': 'Not found'
                }
                return Response(response, status=404)

@api_view(['GET'])
def host_alloc(request, *args, **kwargs):
    if request.method == 'GET':
        # result: give to unknown VNFs a mininet host
        mapped_vnfs = []
        for i in range(0, redis_instance.llen("mapped_vnfs")):
            mapped_vnfs.append(redis_instance.lindex("mapped_vnfs", i))
        if not mapped_vnfs: # None obj, make it into empty list
            mapped_vnfs = []
        free_mn_hosts = redis_instance.get("free_mn_hosts")
        if free_mn_hosts:
            free_mn_hosts = int(free_mn_hosts)
        else:
            free_mn_hosts = 0
        total_mn_hosts = redis_instance.get("total_mn_hosts")
        if total_mn_hosts:
            total_mn_hosts = int(total_mn_hosts)
        else:
            total_mn_hosts = 0
        print(str(total_mn_hosts))
        # get non assigned VNFs
        for key in redis_instance.keys("*"):
            key_string = key
            if key_string.startswith("VNF") and key_string not in mapped_vnfs:
                non_assigned_vnf_ip = redis_instance.get(key)
                free_mn_hosts -= 1
                if free_mn_hosts == 0:
                    response = "ERROR: mininet hosts limit reached! No more free mininet hosts."
                    print(response)
                    return Response(response, status=500)
                # assign the new VNF a mininet host
                redis_instance.set(non_assigned_vnf_ip.replace('.', '-'), "10.70.0." + str((total_mn_hosts - free_mn_hosts)))
                redis_instance.set("10_70_0_" + str((total_mn_hosts - free_mn_hosts)), non_assigned_vnf_ip)
                redis_instance.lpush("mapped_vnfs", key_string)
                mapped_vnfs.append(key_string)

        response = {
            'msg': 'success'
        }
        # update mapped_vnfs and free_mn_hosts values in Redis
        # delete old list first
        while redis_instance.llen("mapped_vnfs"):
            redis_instance.ltrim("mapped_vnfs", 0, -99)
        for el in mapped_vnfs:
            redis_instance.lpush("mapped_vnfs", el)
        redis_instance.set("free_mn_hosts", free_mn_hosts)

        return Response(response, status=200)
    else:
        return Response(response, status=404)

@api_view(['PUT'])
def conntrack(request, *args, **kwargs):
    if request.method == 'PUT':
        # result: give the conntrack
        body = request.body
        item = json.loads(body)
        dst_ip = item["dst_ip"]
        src_ip = item["src_ip"]
        src_port = item["src_port"]
        res = subprocess.run(["sudo", "conntrack", "-L", "--dst", dst_ip, "--src", src_ip], stdout=subprocess.PIPE)
        res = str(res.stdout.decode("utf-8"))
        res = res.split("\\n")
        line = res[0]
        print("res: "+ str(res[0]))
        result = None
        if "tcp" in line and "sport="+str(src_port) in line:
            result = re.search("dst="+dst_ip+" sport="+str(src_port)+" dport=(.*) src", line)
        print(result)
        dst_port = result.group(1)
        response = {
            'msg': dst_port
        }
        return Response(response, status=200)
