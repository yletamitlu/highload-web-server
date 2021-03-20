from server import server
import asyncio


if __name__ == '__main__':
    server = server.Server()
    server.init_connect()
    asyncio.run(server.start())
