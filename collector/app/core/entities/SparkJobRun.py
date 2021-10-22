from dataclasses import dataclass
from sortedcontainers import SortedKeyList

import app.services.helpers.payload_keys as keys

@dataclass
class SparkJobRun:
    """A run of a particular SparkJob."""
    # job_name: str
    # run_id: str
    start_date: int = None
    end_date: int = None
    messages: SortedKeyList = SortedKeyList([], lambda x : x.get(keys.GENERATED_AT))


