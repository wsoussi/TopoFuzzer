# Logging

Katana exports logs in both local host machine and remote log server

## Local Host

Use the command `katana log` to examine logs from both katana-mngr and katana-nbi containers
> Katana writes the logs in files on the localhost, in katana-mngr and katana-nbi directories

## Remote log server

Edit the file [docker-compose.yaml](https://github.com/medianetlab/katana/blob/master/katana-mngr/docker-compose.yaml) in the katana-mngr directory. Uncomment the logging part, replacing the IP, port and protocol of the remote log server (e.g. Graylog).

```YAML
logging:
  driver: syslog
  options:
    syslog-address: "<udp/tcp>://<remote_server_IP>:<port>"
    tag: "Katana_SliceManagerr"
    syslog-format: "rfc5424"

```
