# Arguments of Spark distribution. You should not need to change them.
spark_version = 2.4.4
distribution = spark-${spark_version}-bin-hadoop2.7

# Arguments of the run_* commands. 
# For example, change collector_url to point to your deployed service:
# make collector_url=http://url.of.my.service.com/ run_one_app
job_name = spark-pi
collector_url = http://localhost:5000/collect
n_partitions = 100

${distribution}.tgz:
	@echo "Download Spark distribution..."
	curl -O -L https://archive.apache.org/dist/spark/spark-${spark_version}/${distribution}.tgz

${distribution}: ${distribution}.tgz
	@echo "Extract Spark distribution..."
	tar -zxf ${distribution}.tgz

run_one_app: ${distribution}
	@echo "Run one app..."
	${distribution}/bin/spark-submit --class org.apache.spark.examples.SparkPi \
		--conf spark.extraListeners=co.datamechanics.listener.DataMechanicsListener \
		--jars data-mechanics-listener_2.11-1.0.jar \
		--conf spark.datamechanics.collector.url=${collector_url} \
		--conf spark.datamechanics.apiKey.secret="not_required_for_the_exercise" \
		--conf spark.datamechanics.job.name=${job_name} \
		--conf spark.datamechanics.buffer.maxNumEvents=100 \
		${distribution}/examples/jars/spark-examples_2.11-${spark_version}.jar ${n_partitions} \
		2>&1

run_concurrent_apps: ${distribution}
	make collector_url=${collector_url} job_name=job1 n_partitions=1000 run_one_app & \
	make collector_url=${collector_url} job_name=job2 n_partitions=100 run_one_app & \
	make collector_url=${collector_url} job_name=job3 n_partitions=100 run_one_app & \
	wait
