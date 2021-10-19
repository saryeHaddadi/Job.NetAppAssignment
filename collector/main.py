#!/usr/bin/python
# coding: utf-8

from flask import Flask, request, make_response

from app.compression import gzip_http_request_middleware
from app.logging import print_payload


def create_app():
    app = Flask(__name__)

    # Enable the app to support gzip encoded requests
    app.before_request(gzip_http_request_middleware)

    @app.route('/collect', methods=['POST'])
    def collect():
        '''A collect endpoint that takes as input JSON payloads
        and prints to stdout'''
        print_payload(request.data)
        return make_response({"message": "received"})

    @app.route('/health', methods=['GET'])
    def health():
        return make_response({"message": "alive"})

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000)
