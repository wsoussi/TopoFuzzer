# <img src="./templates/images/LOGO2.png" alt="drawing" width="150"/>  TopoFuzzer - A Network Topology Fuzzer 

-----------------------------------------

## :page_with_curl: What is TopoFuzzer?

TopoFuzzer is a gateway node with two main functionalities:
1. It assists your service (containers or VMs) migration and reinstantiation at the networking level, using an API to update the mapping between the public IP used by users and the private IP allocated to the new instance.
2. It establishes a mininet network allowing for dynamic changes of the network topology to disrupt reconnaissance and scanning of external and internal users.

You can read a detailed presentation of TopoFuzzer

## :clipboard: Features

- REST API to update the mapping between the public IP and the private IP of a service
- Instant handover of TCP connections: _e.g.,_ HTTP/2
- Instant handover of UDP connections: _e.g.,_ QUIC, HTTP/3
- No TLS certificates handling needed for HTTPS/3
- Add and remove nodes, switches, and links dynamically with the mininet API
- Change the traffic flow in the data plane by connecting an external SDN controller 


## :hammer_and_pick: Quick Start

**PREREQUIREMENTS:**
- install redis and configure it to get connected with the external IP of the host (not 127.0.0.1)
- For v0.2 add MANGLE iptables rules

**INSTALL:**
- install with pip

**DEPLOY:**
- change the file `settings.py` to put the host IP and the redis port in the correspondent field `TOPOFUZZER_IP` and `REDIS_PORT` (default port is 6379)
- create an admin user with the command ```python manage.py createsuperuser```
- start the server with the command ````python manage.py runserver 0:8000````, which starts the TopoFuzzer REST API interface
- start the TopoFuzzer mininet and redirection proxies with the command ````python manage.py proxy_handler_main --sdnc-ip <SDNC>```` where _<SDNC>_ is the IP or the hostname of the external SDN controller

**USAGE:**
Now you can transfer open connections to different instances of your service dynamically and control the mininet middle-network using your SDNC.
The usage of TopoFuzzer and the description of the REST API interface is detailed in the Wiki/Documentation here below.

[//]: # ()
[//]: # (## :book: Documentation)

[//]: # ()
[//]: # (- [Wiki]&#40;https://github.com/topofuzzer/wiki&#41;)