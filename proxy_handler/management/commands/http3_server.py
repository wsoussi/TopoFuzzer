# start a python http/3 server using aioquic
#
# usage:
#   python3 -m aioquic.asyncio.server <host> <port>
#
# example:
#   python3 -m aioquic.asyncio.server 0000000 4433
#
# see https://github.com/aioquic/aioquic/pull/659
#
import asyncio
import sys
from typing import Optional
from urllib.parse import urlparse
from urllib.parse import parse_qs

from aioquic.asyncio.client import connect