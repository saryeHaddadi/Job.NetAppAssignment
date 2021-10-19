import json
from pprint import pprint
from ..database import database as db
import bisect

MESSAGES = 'messages'
CONTENT = 'content'
JOB_NAME = 'job_name'
RUN_ID = 'run_id'
i=0

def collect(str_payload):
    payload = json.loads(str_payload)
    insert_payload(payload)

def insert_payload(payload):
    job_name = payload[JOB_NAME]
    run_id = payload[RUN_ID]
    create_if_not_exists(job_name, run_id)
    insert_messages(job_name, run_id, payload[MESSAGES])

def create_if_not_exists(job_name, run_id):
    if db.SparkLogEventTable.get(job_name) is None:
        db.SparkLogEventTable[job_name] = dict()
    if db.SparkLogEventTable[job_name].get(run_id) is None:
            (db.SparkLogEventTable[job_name])[run_id] = []

def insert_messages(job_name, run_id, messages):
    bisect.insort_left(((db.SparkLogEventTable[job_name])[run_id]).append(messages),
                       messages,
                       )
    

def get_jobs():
    return [job_name for job_name in db.SparkLogEventTable.keys()]

def get_run_ids(job_name):
    result = []
    if db.SparkLogEventTable.get(job_name) is not None:
        result = [run_id for run_id in db.SparkLogEventTable.get(job_name)]
    return result

def get_events(job_name, run_id):
    result = []
    if (db.SparkLogEventTable.get(job_name) is not None
        and db.SparkLogEventTable.get(job_name).get(run_id) is not None):
        result = [message for message in db.SparkLogEventTable.get(job_name).get(run_id)]
    return result

