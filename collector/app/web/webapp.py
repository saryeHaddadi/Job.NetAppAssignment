from flask import Flask, request, make_response


from app.services.helpers.compression import gzip_http_request_middleware
from app.services.helpers.logging import print_payload
from app.services.SparkJobAppService import SparkJobAppService



def create_app():
    app = Flask(__name__)
    spak_service = SparkJobAppService()

    # Enable the app to support gzip encoded requests
    app.before_request(gzip_http_request_middleware)

    @app.route('/collect', methods=['POST'])
    def collect():
        """A collect endpoint that takes as input JSON payloads
        and save them on a local in-memory store.

        Returns:
            json: Defaults to 'received'.
        """
        spak_service.collect(request.data)
        #print_payload(request.data)
        return make_response({"message": "received"})

    @app.route('/job', methods=['GET'])
    def get_jobs():
        """Endpoint that returns the list of collected job_names

        Returns:
            json: list of collected job_names
        """
        return make_response({"jobs": spak_service.get_jobs()})

    @app.route('/job/<job_name>', methods=['GET'])
    def get_run_ids(job_name):
        """Endpoint that returns the list of run_ids for a given job_names

        Args:
            job_name (str): The job's name

        Returns:
            json: list of run ids
        """
        return make_response({"run_ids": spak_service.get_run_ids(job_name)})

    @app.route('/job/<job_name>/<run_id>/events', methods=['GET'])
    def get_events(job_name, run_id):
        """Endpoint that returns the list of all events associated to a particular run.
        Events ('message') can either Events, or HearthBeats.
        This endpoint could have been named get_messages.

        Args:
            job_name (str): The job's name
            run_id (str): The desired run

        Returns:
            json: list of events
        """
        return make_response({"events": spak_service.get_events(job_name, run_id)})

    @app.route('/job/<job_name>/<run_id>/duration', methods=['GET'])
    def get_duration(job_name, run_id):
        """Return the duration, in ms, of a particular run.

        Args:
            job_name (str): The job's name
            run_id (str): The desired run

        Returns:
            json: Duration in ms (int)
        """
        return make_response({"duration-ms": spak_service.get_duration(job_name, run_id)})

    @app.route('/health', methods=['GET'])
    def health():
        return make_response({"message": "alive"})
    return app



