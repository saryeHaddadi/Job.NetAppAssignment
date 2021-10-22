
- Endpoint for ingesting. Today, the data is just printed, we want to store it in a DB.
- Implement 4 query endpoints
- Unit tests
- Deploy the service on the cloud



Query endpoints
- get /job
- get /job/{job_name}
- get /job/{job_name}/{run_id}
    -- should respond in linear time woth repect to the returned events
- get /job_duration/{job_name}/{run_id}


In Python, Lists are implemeted as Arrays.
- Time complexity for accessing Lists[i] = constante.

SparkListenerApplicationStart, SparkListenerApplicationEnd


# Next steps & Improvement ideas

messages[]
- .'message_type': 'spark-event'
- .content as json, .Event = SparkListenerApplicationEnd

sarye-netapp-assignment.francecentral.cloudapp.azure.com

