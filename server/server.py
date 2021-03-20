import asyncio
import socket

import uvloop as uvloop

from context import request
from context import response
from utils import config


async def handle(sock):
    raw = await asyncio.get_event_loop().sock_recv(sock, 1024)
    req = request.Request(raw.decode('utf-8'))
    result_code = req.parse_request()
    resp = response.Response(req.method, req.url, req.protocol, req.filepath, result_code)
    await resp.send(sock)


class Server:
    def __init__(self):
        self.host = config.HOST
        self.port = config.PORT
        self.address = f'{self.host}:{self.port}'
        self.server_socket = None

    def init_connect(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(512)
        server_socket.setblocking(False)

        self.server_socket = server_socket
        print(f'server listens on {self.address}')

    async def start(self):
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        while True:
            child_sock, _ = await asyncio.get_event_loop().sock_accept(self.server_socket)
            await handle(child_sock)
            child_sock.close()
