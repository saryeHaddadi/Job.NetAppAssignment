# Home assignement, Sarye

Installation: `kubectl apply -f collector/kube-manifests.yaml`

Example: http://kube-sarye.francecentral.cloudapp.azure.com:32500/health


## Endpoints
- Collect Events: `/collect`
- Get Jobs: `/job`
    - Notes: Requirements didn't mandate that the results be sorted so they are not. For production, I think we should settle on a sort order (either by name, or last run start_date/end_data) depending on the case.
- Get Run IDs: `/job/<job_name>`
- Get Events: `/job/<job_name>/<run_id>/events`
    - Notes:
        - The underlying data stucture (`SortedKeyList`), performs in-order inserts, meaning, we performe the sort operation at write time (= pay a little cost), this will allows us to save the sort operation at read time. At the end, we can respond in linear time with respect to the number of returned events.
        - In Python, Lists are implemented as Arrays. The complexity of searching the target list index while performing the write operation, is with respect to an array data structure, not a list.
- Get Duration: `/job/<job_name>/<run_id>/duration`
    - Notes: At write time when collecting the events, we parsed the message and saved the timestamp of the start & end events (SparkListenerApplicationStart / SparkListenerApplicationEnd) at the root of the run_id, so that the duration can be accessed in constant time by this endpoint.


## Next steps
All endpoints work and satisfy the requirements, we can thus focus on improving the backend in particular, then polishing the client-facing APIs.
1. Persisting the data on disk (endpoint: /collect).
    - Using a relational DB / NoSQL and storing the data in there. The choice is to be determined with the current ecosystem in the company, and the use case.
    - Making a research on the Repository pattern, an implement it. In particular, in the present version, the logic to access the physical data is mixed with the business logic.
2. Read on the best practices on how to handle the HTTP responses when a key do not exists, and discuss this matter with the Lead Dev (returning an empty result, or an HTTP error code).
3. Apply a schema on the controllers input/output, for instance by migrating everything to FastAPI/Pydanic, or making a reseach on how to deal with this in Flask.
4. Read on pytest & fixtures (pytest's way to implement unit testing). Then make one testing class for each method to test. This testing class will have as much test methods as unit tests that we have identified for the method to test.
5. Document the API with Swagger/OpenAPI
6. Extract the `host` & `listening ports` params out of the code, so that they can be treated as configurations.
7. Document all functions, some are not (especially the app/services)
8. Adding a .dockerignore

## Improvement ideas
Splitting the app into 2 different apps. One for collecting the data, and one for serving it.
1. Collecting the data
    - If we have quite a volumetry, and we have other use cases other than just sinking the data into a data store, I would plug the collect API to a message brocker, this would enable the fan-out of the consumption (one of them being sinking the data to a data store). I would then put in front of the message broker a reverse-proxy in order to: 1/ load balance the incomming requests, 2/ and not expose the outside world directly to our internal the message broker.
    - Other example of consumption: sinking the data to an object store for long term storage, feeding a search index, search indexes & logs have always brought value, computing some metrics on the fly and storing them on a relational DB.
2. Transform the kube-manifests into an helm chart.









