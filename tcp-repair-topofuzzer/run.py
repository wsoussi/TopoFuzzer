#!/usr/bin/env python2

import sys, os
import hashlib
from subprocess import Popen, PIPE

str2 = "test_test" * (1 << 20)
str1 = "Test_Test!"

use_ssh = True
ssh = []

src = os.getenv("TCP_SRC", "10.161.1.135")
dst = os.getenv("TCP_DST", "10.161.1.137")
sport = os.getenv("TCP_SPORT", "12345")
dport = os.getenv("TCP_DPORT", "8080")
ssh_key = os.getenv("TCP_SSHKEY", "")

print(sys.argv[1])
args = [sys.argv[1],
        "--addr", src, "--port", sport, "--seq", "555",
        "--next",
        "--addr", dst, "--port", dport, "--seq", "666",
        "--reverse", "--", "./tcp-test.py"]

args.remove("--reverse");

p2 = Popen(args + ["src"], stdout = PIPE, stdin = PIPE)

p2.stdout.read(5)
p2.stdin.write(b'start')

p2.stdin.write(bytes(str2, 'utf-8'))
p2.stdin.close()

stop = "no"
while stop != "yes":
    stop = input("do you want to stop?")

if p2.wait():
    sys.exit(1)

print("PASS")
