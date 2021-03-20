import asyncio
from datetime import datetime
from socket import socket
from utils import consts
from utils import config
import pathlib
import os


class Response:
    def __init__(self, method: str, url: str, protocol: str, filepath: str, code: str):
        self.method = method
        self.url = url
        self.protocol = protocol
        self.filepath = filepath
        self.status_code = code
        self.headers = {
            'Connection': '',
            'Server': '',
            'Date': '',
        }
        self.response = ''
        self.__init_headers()
        self.__make_response()

    def __init_headers(self):
        self.headers['Connection'] = 'Close'
        self.headers['Server'] = config.SERVE_NAME
        self.headers['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')

        if self.status_code == consts.STATUS_OK and self.filepath is not None:
            self.headers['Content-Type'] = consts.CONTENT_TYPES[pathlib.Path(self.filepath).suffix]
            self.headers['Content-Length'] = str(os.path.getsize(self.filepath))

    def __make_response(self):
        self.response = self.protocol + ' ' + str(self.status_code) + ' ' + consts.HTTP_CODES[
            self.status_code] + consts.LINE_SEP

        for header, value in self.headers.items():
            self.response += f'{header}: {value}' + consts.LINE_SEP
        self.response += consts.LINE_SEP

    def __read_file(self):
        with open(self.filepath, 'rb') as f:
            return f.read()

    async def send(self, conn: socket):
        conn.sendall(self.response.encode('utf-8'))
        if self.status_code == consts.STATUS_OK and self.method == consts.METHOD_GET and self.filepath is not None:
            body = self.__read_file()
            await asyncio.get_event_loop().sock_sendall(conn, body)
