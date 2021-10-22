from app.infrastructure.data.dbcontext import SparkJobTable

# TODO
class SparkJobRepository:
    def __ini__(self):
        pass

    def get(self, job_name):
        return SparkJobTable[job_name]
 
    def insert(self, job_name):
        SparkJobTable[job_name] = dict()

