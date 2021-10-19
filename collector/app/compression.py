import gzip
from flask import request


def gzip_http_request_middleware():
    '''Enable the server to support GZIP-compressed requests
    Add it to the app with `app.before_request(gzip_http_request_middleware)'''
    encoding = request.headers.get('content-encoding', '')
    if encoding == 'gzip':
        request._cached_data = gzip.decompress(request.get_data())
