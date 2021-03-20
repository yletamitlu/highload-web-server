from urllib.parse import unquote
from utils import consts
from utils import config
import os


class Request:
    def __init__(self, raw: str):
        self.raw = raw
        self.method = ''
        self.url = ''
        self.protocol = ''
        self.filepath = None

    def parse_request(self):
        strings = self.raw.split('\r\n')
        if strings[0] == '\n':
            return consts.STATUS_FORBIDDEN
        self.method, url, self.protocol = strings[0].split(' ')
        self.url = url
        res = self.validate_method()
        if res != consts.STATUS_OK:
            return res
        res = self.validate_url()
        return res

    def validate_url(self):
        self.url = unquote(self.url.split('?')[0])
        if str(self.url).find('/../') > 0:
            return consts.STATUS_FORBIDDEN

        filepath = os.path.join(config.ROOT_PATH, self.url.lstrip('/'))
        if os.path.isdir(filepath):
            filepath = os.path.join(filepath, 'index.html')
            if not os.path.exists(filepath):
                print(filepath, ' file not found')
                return consts.STATUS_FORBIDDEN
        else:
            if not os.path.isfile(filepath):
                print('file not file')
                return consts.STATUS_NOTFOUND
        self.filepath = filepath
        return consts.STATUS_OK

    def validate_method(self):
        if self.method not in consts.ALLOW_METHODS:
            return consts.STATUS_NOTALLOWED
        return consts.STATUS_OK
