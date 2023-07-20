# <img src="./templates/images/LOGO2.png" alt="drawing" width="150"/>  TopoFuzzer - A Network Topology Fuzzer 

[![License: MIT](https://img.shields.io/static/v1?label=license&message=MIT&color=blue)](https://mit-license.org/)
[![GitHub issues](https://img.shields.io/github/issues/wsoussi/TopoFuzzer)](https://github.com/wsoussi/TopoFuzzer/issues)
[![GitHub forks](https://img.shields.io/github/forks/wsoussi/TopoFuzzer)](https://github.com/wsoussi/TopoFuzzer/network)
[![GitHub stars](https://img.shields.io/github/stars/wsoussi/TopoFuzzer)](https://github.com/wsoussi/TopoFuzzer/stargazers)
[![](https://img.shields.io/static/v1?label=docs&message=passing&color=green)](https://github.com/wsoussi/TopoFuzzer/wiki)
[![](https://sonarcloud.io/api/project_badges/measure?project=wsoussi_TopoFuzzer&metric=alert_status)](https://sonarcloud.io/summary/overall?id=wsoussi_TopoFuzzer)
[![](https://sonarcloud.io/api/project_badges/measure?project=wsoussi_TopoFuzzer&metric=ncloc)](https://sonarcloud.io/summary/overall?id=wsoussi_TopoFuzzer)
[![](https://sonarcloud.io/api/project_badges/measure?project=wsoussi_TopoFuzzer&metric=sqale_index)](https://sonarcloud.io/summary/overall?id=wsoussi_TopoFuzzer)
[![](https://sonarcloud.io/api/project_badges/measure?project=wsoussi_TopoFuzzer&metric=reliability_rating)](https://sonarcloud.io/summary/overall?id=wsoussi_TopoFuzzer)
[![](https://sonarcloud.io/api/project_badges/measure?project=wsoussi_TopoFuzzer&metric=vulnerabilities)](https://sonarcloud.io/summary/overall?id=wsoussi_TopoFuzzer)
[![](https://sonarcloud.io/api/project_badges/measure?project=wsoussi_TopoFuzzer&metric=bugs)](https://sonarcloud.io/summary/overall?id=wsoussi_TopoFuzzer)
[![](https://sonarcloud.io/api/project_badges/measure?project=wsoussi_TopoFuzzer&metric=code_smells)](https://sonarcloud.io/summary/overall?id=wsoussi_TopoFuzzer)
[![](https://sonarcloud.io/api/project_badges/measure?project=wsoussi_TopoFuzzer&metric=sqale_rating)](https://sonarcloud.io/summary/overall?id=wsoussi_TopoFuzzer)

<div style="text-align: center;">
<a href="https://github.com/wsoussi/TopoFuzzer">
<img src="https://raw.githubusercontent.com/wsoussi/TopoFuzzer/main/templates/images/github_logo_icon.png">
</a>
<a href="https://sonarcloud.io/summary/overall?id=wsoussi_TopoFuzzer">
<img src="https://sonarcloud.io/images/project_badges/sonarcloud-black.svg">
</a>
</div>

-----------------------------------------

## :page_with_curl: What is TopoFuzzer?

TopoFuzzer is a gateway node with two main functionalities:
1. It assists your service (containers or VMs) migration and reinstantiation at the networking level, mapping the public IP used by users to connect and the private IP allocated to the new instance. The advantage of TopoFuzzer is the live handover of connections without having to close them and re-establish them. This is critical for a seamless migration of services with long lived connections.
2. It establishes a mininet network allowing for dynamic changes of the network topology to disrupt reconnaissance and scanning of external and internal attackers with Moving Target Defense (MTD) strategies.


## :clipboard: Features

- REST API to update the mapping between the public IP and the private IP of a service
- Instant handover of TCP connections: _e.g.,_ HTTP/2
- Instant handover of UDP connections: _e.g.,_ QUIC, HTTP/3
- No TLS certificates needed for HTTPS/3 (no trust on the intermediary needed)
- Add and remove nodes, switches, and links dynamically with the mininet API
- Change the traffic paths in the data plane by connecting an external SDN controller 


## :hammer_and_pick: Quick Start

**REQUIREMENTS:**
- Operating System: Ubuntu 18.04
- Python3.6.9 (```sudo apt install python3.6```)
- Python3-pip (```sudo apt install python3-pip```)
- Python3-virtualenv (```pip3 install virtualenv```)
- Mininet 2.3.0 (follow option 2  of the mininet guide http://mininet.org/download/)
- redis (```sudo apt install redis```). Set redis to use the external IP of your machine or VM. To do this edit ```/etc/redis/redis.conf```
 by changing the line ```bind 127.0.0.1::1``` to ```bind 0.0.0.0``` and uncommenting ```# requirepass <yourpassword>```. Then restart redis with `sudo /etc/init.d/redis-server restart`.

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
   pip3 install -r requirements.txt
   ```


## Deploy TopoFuzzer

1. change the file `TopoFuzzer/settings.py` to put the host IP and the redis port in the correspondent field `TOPOFUZZER_IP`, `REDIS_PORT` (default port is 6379), and `REDIS_PASSWORD` to _\<yourpassword\>_.
2. also in `TopoFuzzer/settings.py`, add the public IP of your hosting machine to `ALLOWED_HOSTS`.
3. start the _sqlite3_ DB with `python3 manage.py makemigrations` and `python3 manage.py migrate`.
4. create an admin user with the command ```python manage.py createsuperuser```.
5. start the server with the command ````python manage.py runserver 0:8000````, which starts the TopoFuzzer REST API interface. 

**Deploy the mininet _"fuzzing network"_ with isolated redirection proxies per service**

4. start the TopoFuzzer mininet middle network and the redirection proxies per service with the command ````sudo python manage.py proxy_handler_main --sdnc-ip <SDNC>```` where _\<SDNC\>_ is the IP or the hostname of the external SDN controller
-> For a mininet local default controller remove the --sdnc-ip option.

## Errors
If the error ```Êxception: Could not find a default OpenFlow controller``` occurs, try:
```bash
   sudo apt-get install openvswitch-testcontroller
   ```
```bash
   sudo cp /usr/bin/ovs-testcontroller /usr/bin/ovs-controller
   ```
If the error ```Exception: Please shut down the controller which is running on port 6653:``` occurs at starting the mininet:
```bash
   sudo fuser -k 6653/tcp
   ```
If Syntax error while runnning a manag.py ... command then you either have to activate the virtual environment or keep the path if the command required sudo
```bash
   sudo -E env "PATH=$PATH" python3 manage.py proxy_handler_main
   ```
 If port already in use (not from a different tool but because of a lost ssh connection etc)
 ```bash
   sudo fuser -k 8000/tcp
   ```
   
**Deploy a single redirection proxy for all services (available in v0.2)**

This option is convenient when the isolation of traffic between services is not relevant and allows to reduce the CPU consumption by at least 20 fold (for 4 services and over). The main reason is that only one proxy and listener is deployed for all the services.
4. Add TPROXY mangling rule with the command ````sudo iptables -t mangle -I PREROUTING ! -s <host_IP> -d <services_public_IP_range> -p tcp -j TPROXY --on-port=5555 --on-ip=127.0.0.1````
5. add _net_admin_ rights to the redirection proxy with ````sudo setcap cap_net_raw,cap_net_admin=eip proxy_handler/management/commands/singleHostProxy.py````
6. Start the single redirection proxy using the command ````sudo python manage.py singleHostProxy````

> Sudo privileges will be needed to run the script with _net_admin_ rights

## :book: Usage and documentation:
Now you can transfer open connections to different instances of your service dynamically and control the mininet middle-network using your SDNC.
More details on the deployment, the usage of TopoFuzzer, and the description of the REST API interface is detailed in the Wiki/Documentation here: [Wiki](https://github.com/wsoussi/TopoFuzzer/wiki)

## Citing the Project:
To cite this repository in publications:

```bibtex
@INPROCEEDINGS{10154367,
  author={Soussi, Wissem and Christopoulou, Maria and Anagnostopoulos, Themis and Gür, Gürkan and Stiller, Burkhard},
  booktitle={NOMS 2023-2023 IEEE/IFIP Network Operations and Management Symposium}, 
  title={TopoFuzzer — A Network Topology Fuzzer for Moving Target Defense in the Telco Cloud}, 
  year={2023},
  volume={},
  number={},
  pages={1-5},
  doi={10.1109/NOMS56928.2023.10154367}}
```

