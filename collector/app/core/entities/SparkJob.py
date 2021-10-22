from dataclasses import dataclass

from app.core.entities.SparkJobRun import SparkJobRun

@dataclass
class SparkJob:
    """A Spark Job whose events have been collected (at least partially)."""
    
    """The Spark Job name
    """
    job_name: str
    
    """A dictionnary of all runs known for the job.
    In a database, SparkJobRun would have a foreign key to SparkJobRun.
    """
    runs: dict[SparkJobRun.run_id, SparkJobRun]



