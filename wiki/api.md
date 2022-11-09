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
TopoFuzzer, to distinguish private IPs from public IPs in the bidirectional mapping, it changes the IP string by replacing `.` with `-` for public IPs and with `_` for private IPs. This also allows to write the IPs in the URL path as `.` can only be used in the FQDN part of an URL.

## Examples


### GET - api/mappings

```bash
    curl --location --request GET 'http://<topofuzzer_ip>:8000/api/mappings' \
    --header 'Content-Type: text/plain'
````

This will return everything related to TopoFuzzer: the services' public IPs and their mappings to private IPs.


