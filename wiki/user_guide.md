# User Guide

## Requirements

Install TopoFuzzer on Ubuntu 18.04 Operating System. Further requirements before the installation are:
- Python3.6.9 (```sudo apt install python3.6```)
- Python3-pip (```sudo apt install python3-pip```)
- Mininet 2.3.0 (follow option 2  of the mininet guide http://mininet.org/download/)
- redis (```sudo apt install redis```). Set redis to use the external IP of your machine or VM.


## Install TopoFuzzer

Use the following commands to install TopoFuzzer:
1. ```bash 
   git clone https://github.com/wsoussi/TopoFuzzer.git
   ```
2. ```bash
   git checkout v0.1-fixes
   ```
3. ```bash
   python3.6 -m virtualenv venv
   ```
4. ```bash
   source venv/bin/activate
   ```
5. ```
   pip install -r requirements.txt
   ```


## Deploy TopoFuzzer

1. change the file `settings.py` to put the host IP and the redis port in the correspondent field `TOPOFUZZER_IP` and `REDIS_PORT` (default port is 6379)
2. create an admin user with the command ```python manage.py createsuperuser```
3. start the server with the command ````python manage.py runserver 0:8000````, which starts the TopoFuzzer REST API interface 

**Deploy the mininet _"fuzzing network"_ with isolated redirection proxies per service**

4. start the TopoFuzzer mininet middle network and the redirection proxies per service with the command ````python manage.py proxy_handler_main --sdnc-ip <SDNC>```` where _\<SDNC\>_ is the IP or the hostname of the external SDN controller


**Deploy a single redirection proxy for all services (available in v0.2)**

This option is convenient when the isolation of traffic between services is not relevant and allows to reduce the CPU consumption by at least 20 fold (for 4 services and over). The main reason is that only one proxy and listener is deployed for all the services.
4. Add TPROXY mangling rule with the command ````sudo iptables -t mangle -I PREROUTING ! -s <host_IP> -d <services_public_IP_range> -p tcp -j TPROXY --on-port=5555 --on-ip=127.0.0.1````
5. add _net_admin_ rights to the redirection proxy with ````sudo setcap cap_net_raw,cap_net_admin=eip proxy_handler/management/commands/singleHostProxy.py````
6. Start the single redirection proxy using the command ````sudo python manage.py singleHostProxy````

> Sudo privileges will be needed to run the script with _net_admin_ rights

## Use TopoFuzzer

There are three ways to interact with Katana Slice Manager: The REST API and the web GUI API. The administrator has to prepare the system before starting the traffic redirection. The prepatation phase includes defining the IP range to use for mininet so that mininet hosts are allocated with the public IPs used by the services.


### Register the available platform locations

The first step for the Katana/Platform administrator is to register the available Platform locations. These [locations](location) will be used at a later stage for registering platform components and, eventually, deploying network slices.


### Add/remove services to place behind TopoFuzzer and Update the IP Mapping 

Refer to the [REST API page](api) for the interaction with TopoFuzzer.


### Logs

The logs are generated in two files for each service, one for TCP traffic and one for UDP.


### Stop

To stop TopoFuzzer you have to exit the mininet console when using mininet traffic isolation:

```bash
mininet> exit
```
For the one-for-all method (in v0.2) simply use ````Ctrl+C````.


### Uninstall

As we started TopoFuzzer with a ````venv```` environment, to go back to the python interpreter use

```bash
$ deactivate
```


