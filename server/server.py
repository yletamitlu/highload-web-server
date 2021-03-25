import asyncio
import atexit
import os
import signal
import socket

import uvloop as uvloop

from context import request
from context import response
from utils import config
from utils.logger import logger


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
        self.process_pull = []
        atexit.register(self.kill_children)

    def init_connect(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen()
        server_socket.setblocking(False)

        self.server_socket = server_socket
        logger.info(f'Server listens on {self.address}')

    def prefork(self):
        for i in range(config.CPU_LIMIT):
            pid = os.fork()
            if pid == 0:
                logger.info(f'New child pid: {pid}')
                asyncio.run(self.handle_child())
            else:
                self.handle_parent(pid)

        for pid in self.process_pull:
            print('waidpid', pid)
            os.waitpid(pid, 0)

    def handle_parent(self, pid: int):
        self.process_pull.append(pid)

    async def handle_child(self):
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        while True:
            child_sock, _ = await asyncio.get_event_loop().sock_accept(self.server_socket)
            await handle(child_sock)
            child_sock.close()

    def kill_children(self):
        for pid in self.process_pull:
            logger.info(f'Kill pid: {pid}')
            os.kill(pid, signal.SIGKILL)
