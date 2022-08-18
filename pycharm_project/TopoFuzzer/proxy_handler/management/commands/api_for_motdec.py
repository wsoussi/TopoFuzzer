from django.core.management.base import BaseCommand
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','my_django_project.settings')
import django
from django.conf import settings
import redis
django.setup()
from flask import Flask, request, jsonify, Response

# the host of the API server
HOST = "10.161.1.135"

# Connect to our Redis instance
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0)

api = Flask(__name__)

@api.route('/', methods=['GET'])
def index():
    return Response(
        mimetype='application/json',
        status=200
    )

@api.route('/mapping/update/<value>', methods=['PUT', 'DELETE'])
# manage mapping of a VNF IP and port
def manage_mapping(key):
    if request.method == 'PUT':


@api.route('/mapping/update', methods=['POST'])
# update mapping of a VNF IP and port
def update_ip_mapping():
    print("received POST request")
    content = request.json
    public_ip = content['public_ip']
    new_private_ip = content['new_private_ip']
    # update the mapping
    ip_mapping[public_ip] = new_private_ip
    return jsonify({"update": "done"})

class Command(BaseCommand):
    def handle(self, *args, **options):
        ## start API for proxy management
        api.run(host=HOST, port = 5000) # port is 5000