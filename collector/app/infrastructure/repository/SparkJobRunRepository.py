from app.infrastructure.data.dbcontext import SparkJobTable

class SparkJobRepository:
    def __ini__(self):
        pass
    

    
    def insert(self, job_name):
        SparkJobTable[job_name] = dict()


