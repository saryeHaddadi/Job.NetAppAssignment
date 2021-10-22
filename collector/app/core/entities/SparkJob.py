from dataclasses import dataclass

from app.core.entities.SparkJobRun import SparkJobRun

@dataclass
class SparkJob:
    """A Spark Job that has been run."""
    job_name: str
    runs: dict[str, SparkJobRun]



