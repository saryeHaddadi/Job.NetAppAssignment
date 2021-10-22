from dataclasses import dataclass
from sortedcontainers import SortedKeyList

import app.services.helpers.payload_keys as keys

@dataclass
class SparkJobRun:
    """A run of a particular SparkJob."""
    
    """The Spark Job name
    """
    job_name: str = None
    
    """The run ID of this instance. (job_name, run_id) form a logical unit.
    """
    run_id: str = None
    
    """Start of the Spark Job run, as a unix timestamp, in miliseconds.
    """
    start_date: int = None
    
    """End of the Spark Job run, as a unix timestamp, in miliseconds.
    """
    end_date: int = None
    
    """List of all messages collected for this (job_name, run_id).
    Here the underlying data structure is a sorted liste, so that the data is
    stored already sorted, in order to save while reading.
    Sort key: 'generated_at'.
    """
    messages: SortedKeyList = SortedKeyList([], lambda x : x.get(keys.GENERATED_AT))


