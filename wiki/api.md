# North Bound Interface REST APIs

You can reach TopoFuzzer at **[http://<topofuzzer_ip>:8000](http://<katana_ip>:8000)** using the REST APIs listed below:

| Method | URI                  | Data | Description                                                          |
|--------|----------------------|------|----------------------------------------------------------------------|
| GET    | /api/mappings        | -    | Returns a list of the services behind TopoFuzzer and the IP mappings |
| POST   | /api/mappings/       | -    | Add mapping between the private and public IPs of a service          |
| PUT    | /api/mappings/\<IP\> | -    | Update the mapping of an IP                                          |
| GET    | /api/host_alloc      | -    | Allocate a mininet host to proxy a service with its public IP        |

TopoFuzzer maintains the mapping between private and public IPs.
Public IPs are predefined for each service as they remain fixed
during a migration or re-instantiation. When a service is deployed, the pri-
vate IP assigned is given to the TopoFuzzer. If the service is
deployed for the first time, a new mapping is registered and
the public IP is assigned to a new vNIC, which will be used
by an instance of the 2-socket proxy. If the service is already
deployed, only the mapping is updated, while the vNIC and
the proxy instance are preserved. 

The mapping is a hash table implemented with Redis and using two entries per one mapping (i.e., pubIP→privIP and
privIP→pubIP). This allows fetching the IP addresses in both directions with a constant complexity (i.e., O(1)).
TopoFuzzer, to distinguish private IPs from public IPs in the bidirectional mapping, it changes the IP string by replacing `.` with `_` for public IPs and with `-` for private IPs. This also allows to write the IPs in the URL path as `.` can only be used in the FQDN part of an URL.

Since there is no delete option available using the api at the moment you have to connect to the redis server and manually clear the mappings.
To connect:
```
redis-cli -a topofuzzer
```
When connected:
```
flushall
```

## Examples

GET - api/mappings
```bash
    curl --location --request GET 'http://<topofuzzer_ip>:8000/api/mappings' \
    --header 'Content-Type: text/plain'
````
Python
```bash
    import requests
    url = "http://" + topofuzzer_ip + ":" + topofuzzer_port + "/api/mappings/"
    response = requests.get(url)
    data = response.json()
````
This will return everything related to TopoFuzzer: the services' public IPs and their mappings to private IPs.

### POST
```bash
    curl --location --request POST 'http://localhost:8000/api/mappings/' --header 'Content-Type: application/json' --data-raw '{"10-161-2-102": "10.70.0.3"}'
```
Python
```bash
    import requests
    url = "http://" + topofuzzer_ip + ":" + topofuzzer_port + "/api/mappings/"
    payload = {
            public_ip: private_ip #For example: 10_10_0_1 : 10.10.0.2
        }
    requests.post( url, json=payload)
````

### PUSH
```bash
    curl --location --request PUT 'http://localhost:8000/api/mappings/<public_IP>' --header 'Content-Type: application/json' --data-raw '{"new_ip": "10.10.0.3"}'
```
```bash
    import requests
    url = "http://" + topofuzzer_ip + ":" + topofuzzer_port + "/api/mappings/"
    payload = {
            "new_ip": private_ip #no encodeing like 10.10.0.3
        }
    requests.put( url + public_ip, json=payload) # public_ip has to be encoded like 10_10_0_1
````
Therby the public_IP has to be encoded like 192_168_0_1.

