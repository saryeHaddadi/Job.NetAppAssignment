#!/usr/bin/python
# coding: utf-8

from flask import Flask, request, make_response

from app.helpers.compression import gzip_http_request_middleware
from app.DAL.logging import print_payload
from app.DAL import SparkLogEvent

def create_app():
    app = Flask(__name__)

    # Enable the app to support gzip encoded requests
    app.before_request(gzip_http_request_middleware)

    @app.route('/collect', methods=['POST'])
    def collect():
        '''A collect endpoint that takes as input JSON payloads
        and prints to stdout'''
        SparkLogEvent.collect(request.data)
        #print_payload(request.data)
        return make_response({"message": "received"})

    @app.route('/job', methods=['GET'])
    def get_jobs():
        return make_response({"jobs": SparkLogEvent.get_jobs()})

    @app.route('/job/<job_name>', methods=['GET'])
    def get_run_ids(job_name):
        return make_response({"run_ids": SparkLogEvent.get_run_ids(job_name)})

    @app.route('/job/<job_name>/<run_id>', methods=['GET'])
    def get_events(job_name, run_id):
        return make_response({"events": SparkLogEvent.get_events(job_name, run_id)})



    @app.route('/health', methods=['GET'])
    def health():
        return make_response({"message": "alive"})
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
