# TopoFuzzer Versions

## Current versions
**TopoFuzzer v0.1**
- REST API to update the mapping between the public IP and the private IP of a service
- Instant handover of TCP connections: _e.g.,_ HTTP/2
- Instant handover of UDP connections: _e.g.,_ QUIC, HTTP/3
- No TLS certificates needed for HTTPS/3 (no trust on the intermediary needed)
- Add and remove nodes, switches, and links dynamically with the mininet API
- Change the traffic paths in the data plane by connecting an external SDN controller

**TopoFuzzer v0.2**
- Reduced QoS overhead by using TPROXY instead of "conntracked" port forwarding to redirect connections towards any ports of the service
- Option of one proxy node for all services behind TopoFuzzer. This reduces the isolation of the services' traffic in compense for a huge CPU usage reduction of 20 fold and over (as services are increasing) 
- 
## Versioning policy

TopoFuzzer follows the Semantic Versioning 2.0.0 policy:
Given a version number MAJOR.MINOR.PATCH, increment the:

1. MAJOR version when you make incompatible API changes,
1. MINOR version when you add functionality in a backwards-compatible manner, and
1. PATCH version when you make backwards-compatible bug fixes.
Additional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR.PATCH format.

For more details visit [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
