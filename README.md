# Home assignement, Sarye

Installation: `kubectl apply -f collector/kube-manifests.yaml`
Example: http://kube-sarye.francecentral.cloudapp.azure.com:32500


**Endpoints**
- Collect Events: `/collect`
- Get Jobs: `/job`
    - Notes: Requirements didn't mandate that the results be sorted so they are not. For production, I think we should settle on a sort order (either by name, or last run start_date/end_data) depending on the case.
- Get Run IDs: `/job/<job_name>`
- Get Events: `/job/<job_name>/<run_id>/events`
    - Notes:
        - The underlying data stucture (`SortedKeyLis`), performs in-order inserts, meaning, the rows are stored sorted. So we performe the sort operation at write time (= pay a little cost, this will allows us we save the sort operation at read time. At the end, we can respond in linear time with respect to the number of returned events.
        - In Python, Lists are implemented as Arrays. The complexity of searching in the write while performing the write operation, is with respect to an array data structure, not a list.
- Get Duration: `/job/<job_name>/<run_id>/duration`
    - Notes: At write time when collecting the events, we parsed the message and saved the timestamp of the start & end events (SparkListenerApplicationStart / End) at the root of the run_id, so that the duration (end-start) can be accessed in constant time by this endpoint.


# Next steps
All endpoints work and satisfy the requirements, we can thus focus on improving the backend in particular, then polishing the client-facing APIs.
1. Persisting the data on disk (endpoint: /collect).
    - Using a relational DB and storing the data in there.
    - Make a research on the Repository pattern, an implement it. In particular, in the present version, the logic to access the physical data is mixed with the business logic.
2. Read on the best practices on how to handle the HTTP responses when a key do not exists, and discuss this matter with the Lead Dev (returning an empty result, or an HTTP error code).
3. Read on pytest & fixtures (pytest's way to implement unit testing). then making one testing class for each method to test. This testing class will have as much test methods as unit tests that we have identified for the method to test.
4. Document the API with Swagger/OpenAPI
5. Extract the host & listening ports out of the code, so they can be treated as configurations.

# Improvement ideas
Splitting the app into 2 different apps. One for collecting the data, and one for serving it.
1. Collecting the data
    - If we have quite a volumetry, and we have other use cases other than sinking the data on a data store, I would plug in collect API to message brocker, this would enable the fan-out of the consummation (one of them being sinking the data to a data store). In would put in front of the message broker a reverse-proxy to load balance the incomming requests, and to not expose the outside world directly to the message broker.
    - Other example of consumption: sinking the data to an object store for long term storage, feeding a search index, search indexes & logs have always brought value, computing some metrics on the fly and storing them on a relational DB.
2. Transform the manifests into helm charts.









