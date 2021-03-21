import asyncio

from server import server


if __name__ == '__main__':
    server = server.Server()
    server.init_connect()
    server.prefork()
