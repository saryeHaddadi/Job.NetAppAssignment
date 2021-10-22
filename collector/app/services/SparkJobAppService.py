import json
from app.infrastructure.data.dbcontext import SparkJobTable
from app.core.entities.SparkJob import SparkJob
from app.core.entities.SparkJob import SparkJobRun
import app.services.helpers.payload_keys as keys


import app.services.helpers.payload_keys as keys

class SparkJobAppService:
    def __init__(self):
        pass

    def collect(self, str_payload):
        payload = json.loads(str_payload)
        self.insert_payload(payload)

    def insert_payload(self, payload):
        job_name = payload[keys.JOB_NAME]
        run_id = payload[keys.RUN_ID]
        self.create_if_not_exists(job_name, run_id)
        self.insert_messages(job_name, run_id, payload[keys.MESSAGES])

    def create_if_not_exists(self, job_name, run_id):
        if SparkJobTable.get(job_name) is None:
            SparkJobTable[job_name] = dict()
        if SparkJobTable[job_name].get(run_id) is None:
                (SparkJobTable[job_name])[run_id] = SparkJobRun()

    def insert_messages(self, job_name, run_id, messages):
        for message in messages:
            SparkJobTable[job_name][run_id].messages.add(message)
            self.check_if_start_or_end_event(message, job_name, run_id)

    def check_if_start_or_end_event(self, message, job_name, run_id):
        if message[keys.MESSAGE_TYPE] == 'spark-event':
            content = json.loads(message[keys.CONTENT])
            if content[keys.EVENT] == 'SparkListenerApplicationStart':
                (SparkJobTable[job_name])[run_id].start_date = content[keys.TIMESTAMP]
            if content[keys.EVENT] == 'SparkListenerApplicationEnd':
                (SparkJobTable[job_name])[run_id].end_date = content[keys.TIMESTAMP]

    def get_jobs(self):
        return [job_name for job_name in SparkJobTable.keys()]

    def get_run_ids(self, job_name):
        if SparkJobTable.get(job_name) is None:
            return []
        else:
            return [run_id for run_id in SparkJobTable.get(job_name)]

    def get_events(self, job_name, run_id):
        if SparkJobTable.get(job_name) is None:
            return []
        elif SparkJobTable.get(job_name).get(run_id) is None:
            return []
        else:
            return list(SparkJobTable.get(job_name).get(run_id).messages.irange())

    def get_duration(self, job_name, run_id):
        if SparkJobTable.get(job_name) is None:
            return None
        elif SparkJobTable.get(job_name).get(run_id) is None:
            return None
        else:
            print('SARYE')
            start_date = (SparkJobTable[job_name])[run_id].start_date
            end_date = (SparkJobTable[job_name])[run_id].end_date
            print(start_date)
            print(end_date)
            if start_date is None or end_date is None:
                return None
            else:
                return end_date - start_date

