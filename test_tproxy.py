import socket

IP_TRANSPARENT = 19

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.IPPROTO_IP, IP_TRANSPARENT, 1)

s.bind(('127.0.0.1', 5555))
s.listen(32)
print("[+] Bound to tcp://127.0.0.1:5555")
while True:
    c, (r_ip, r_port) = s.accept()
    l_ip, l_port = c.getsockname()
    print("[ ] Connection from tcp://%s:%d to tcp://%s:%d" % (r_ip, r_port, l_ip, l_port))
    c.send(b"hello world\n")
    c.close()
