METHOD_GET = 'GET'
METHOD_HEAD = 'HEAD'

ALLOW_METHODS = [METHOD_GET, METHOD_HEAD]

STATUS_OK = 200
STATUS_FORBIDDEN = 403
STATUS_NOTFOUND = 404
STATUS_NOTALLOWED = 405

HTTP_CODES = {
    STATUS_OK: 'OK',
    STATUS_FORBIDDEN: 'Forbidden',
    STATUS_NOTFOUND: 'Not Found',
    STATUS_NOTALLOWED: 'Method Not Allowed',
}

CONTENT_TYPES = {
    '.js': 'application/javascript',
    '.html': 'text/html',
    '.txt': 'text/htm',
    '.css': 'text/css',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.swf': 'application/x-shockwave-flash',
}

HTTP = 'HTTP/'

LINE_SEP = '\r\n'
