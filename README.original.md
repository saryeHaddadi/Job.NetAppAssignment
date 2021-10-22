# Data Mechanics take-home assignments for backend engineers

Thanks for applying! 

For the integrity of the process, please do not distribute or make public the assignment. Thank you!

## Context

At Data Mechanics, we continuously optimize the Spark jobs run on the platform by our users.
When a Spark application is run, the Spark driver produces tons of interesting events (the [Spark events](https://spark.apache.org/docs/latest/monitoring.html#viewing-after-the-fact)) about what happens during the lifetime of the app (what tasks are run, when, their duration, etc).
We leverage those events to understand the inner workings of a Spark application and to change the [configuration](https://spark.apache.org/docs/latest/configuration.html) for the next run of the app.

To collect the Spark events, we have developed a Spark listener (here's the [source code](https://github.com/datamechanics/old-data-mechanics-listener) and more [info](https://mallikarjuna_g.gitbooks.io/spark/content/spark-SparkListener.html) on Spark listeners) that runs alongside a Spark application and streams the events to Data Mechanics backend service.

The goal of this exercise is to implement a portion of this backend service: ingest the events streamed by the listener, store them, and offer a simple API to query them.

> The Spark listener provided in this exercise is actually an old version. Today we use the [Delight listener](https://github.com/datamechanics/delight) to collect event logs and power [Delight](https://www.datamechanics.co/delight), our free monitoring tool for Spark.

## Your task

In `collector/`, we offer a stub of the backend service. For now, it listens to events from the Spark listener and prints them to stdout.

Your mission is to turn this stub into an API that ingests Spark events and offers endpoints for querying them.

- Expose an endpoint for ingesting Spark events sent by the Data Mechanics listener
- Implement four API endpoints that respond to the queries described below
- Unit test the service
- Deploy the service on a cloud of your choice, and send us the IP/URL so that we can try it out

> That's totally fine if you store Spark events on the disk. If you feel like it, you may use another solution like a DB or an object store. But the exercise is already long, so make sure not to create yourself an overwhelming workload!

To submit your solution, you can either create a GitHub repo and give us access to it, or send us the code as a zip file.

### The queries

A job is a logical Spark application that is periodically run by the user. It is uniquely identified by a `job_name`.
For instance, the user can have a job `morning-dashboard` that runs everyday at 6am to prepare data for analysts.

A `run_id` uniquely identifies a given execution (a "run") of a Spark application.
For instance, the run of `morning-dashboard` on July 25th, 2019.

Here are the queries that the backend service must support:

- Return the list of `job_name`s of all jobs stored by the service.
- Provided a `job_name`, return the list of `run_id`s of associated Spark applications
- Provided a `job_name` and a `run_id`, return all Spark events associated to the Spark application
  - The events should be returned as JSON blobs, one per line
  - The events should be returned sorted by the time at which they were generated (see the field `generated_at` in the payload description below)
  - This endpoint should return in linear time with respect to the number of returned events.
- Provided a `job_name` and a `run_id`, return the duration of the Spark application
  - This endpoint should return in constant time.

This is the type of queries that a dashboard webapp would make to the backend service to display information about Spark applications to the users of Data Mechanics.

### Simplifying assumptions

- If the service crashes during a Spark application, it's okay if it loses some Spark events. Upon restart though, if the Spark application is still alive and sending Spark events, the service should resume and append the incoming events to the existing (but incomplete) log.
- You will always receive a `SparkListenerApplicationEnd` event when the application finishes.
- The Spark events related to a single application fit in the random-access memory.

### What we'll evaluate

Beyond correctness, we expect your code to be production-ready and unit tested. 
You should feel good enough about your code to present it to your teammates in a pull-request.

In particular, we'll pay attention to:

- Readability (naming, comments, complexity management)
- Maintainability (modularity, avoiding repetitions)
- Pragmatism (not reinventing the wheel, conciseness)
- Management of edge cases in the API
- Relevance and coverage of unit tests

Please limit your effort to 6 hours and provide a README with next steps and improvement ideas. We'll take those into account in our evaluation!

## Provided code

### Backend service

Folder `collector/` contains a working stub of the backend service.

It contains a catch-all endpoint that ingests payloads from the Spark listener and prints them to the standard output.

The service is implemented as a Flask server, feel free to use another library (or even another language), provided you do not lose too much time because of this choice.

`make serve` spins up the server, listening on port 5000.

This script assumes that you have a version of Python 3 accessible in the shell via the `python` command.
The first time you run it, it will create a virtual environment.

`make test` runs the unit tests.

### Local Spark applications

Folder `spark-app-example` contains a Makefile to run a Spark applications that will stream events to the local collector backend service.

- Run `make run_one_app` to run a dummy Spark app that streams events to `http://localhost:5000/collect`
- Run `make run_concurrent_apps` to run several apps in parallel

These commands assume that you have `curl` and `tar` available on your machine, and a JDK installed.
The first time you run them, a Spark distribution will be downloaded.

### What you should do to test your setup

From folder `collector/`, run
```bash
make serve
```

In another terminal, from folder `spark-app-example/, run
```bash
make run_one_app
```

If you see events being printed in the first terminal, you're all set.
Let us know if something does not work as expected!

## More information about Spark events and the listener payloads

### Spark events

The events are strings containing a JSON object.
Their definition can be found [here](https://github.com/apache/spark/blob/100fc58da54e026cda87832a10e2d06eaeccdf87/core/src/main/scala/org/apache/spark/scheduler/SparkListener.scala) in Spark source code.

Here's a typical event, `SparkListenerTaskStart`:

```json
{
  "Event": "SparkListenerTaskStart",
  "Stage Attempt ID": 0,
  "Stage ID": 0,
  "Task Info": {
    "Accumulables": [],
    "Attempt": 0,
    "Executor ID": "driver",
    "Failed": false,
    "Finish Time": 0,
    "Getting Result Time": 0,
    "Host": "localhost",
    "Index": 51,
    "Killed": false,
    "Launch Time": 1571838437737,
    "Locality": "PROCESS_LOCAL",
    "Speculative": false,
    "Task ID": 51
  }
}
```

For this exercise, the most interesting events are `SparkListenerApplicationStart` and `SparkListenerApplicationEnd`.
They mark the beginning and end of a Spark application.
They both contain a `Timestamp` field.

```json
{ "Event": "SparkListenerApplicationEnd", "Timestamp": 1571838233591 }
```

### Payloads from the Data Mechanics listener

Data Mechanics Spark listener sends data to the server in gzipped POST payloads.
The content is a JSON object containing several messages (ie several Spark events).

There are two types of messages (indicated by `message_type`): `spark-event` and `heartbeat`.
Heartbeats are sent by the agent every 10s to signal the application is not dead (just discard the heartbeats as we assume that there always exists a `SparkListenerApplicationEnd` event in this exercise).
`spark-event` messages each contain a Spark event as a string in the `content` field.

Every payload contains `job_name` and `run_id` fields, that together uniquely represent a run of a Spark application.

Here's an example of payload sent by the listener:

```json
{
  "counters": { "message_counter": 210, "payload_counter": 3 },
  "job_name": "spark-pi",
  "messages": [
    {
      "content": "<spark-event-json-as-a-string>",
      "generated_at": 1571838232674,
      "message_type": "spark-event"
    },
    {
      "content": "<spark-event-json-as-a-string>",
      "generated_at": 1571838232674,
      "message_type": "spark-event"
    },
    "..."
  ],
  "run_id": "local-1571838229751",
  "sent_at": 1571838233591
}
```
