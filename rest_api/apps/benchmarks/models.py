from django.db import models
import shortuuid
import hashlib


class Benchmark(models.Model):

	benchmark_id = models.BigAutoField(primary_key=True)

	bench = (
		('PgBench', 'PgBench'),
		('TBD', 'Something else')
		)

	# displays as char in Postgres, plain enum datatypes are not supported in Django
	benchmark_type = models.CharField(max_length=10, blank=False, choices=bench)

	benchmark_config = models.BigIntegerField(blank=False)


class PgBenchBenchmark(models.Model):

	pgbench_benchmark_id = models.BigAutoField(primary_key=True)

	clients = models.IntegerField()
	init = models.IntegerField()
	warmup = models.IntegerField(null=True)
	#runs = models.IntegerField()
	scale = models.IntegerField()
	duration = models.FloatField()


class PgBenchResult(models.Model):

	pgbench_result_id = models.AutoField(primary_key=True)

	run_id = models.ForeignKey('runs.RunInfo', on_delete=models.CASCADE)

	tps = models.FloatField()
	mode = models.CharField(max_length=100)
	threads = models.IntegerField()
	clients = models.IntegerField()
	latency = models.FloatField()
	read_only = models.BooleanField()
	start = models.FloatField()
	end = models.FloatField()
	run = models.IntegerField()


class PgBenchRunStatement(models.Model):

	pgbench_run_statement_id = models.AutoField(primary_key=True)

	result_id = models.ForeignKey('benchmarks.PgBenchResult', on_delete=models.CASCADE)
	line_id = models.IntegerField(null=True)
	latency = models.FloatField(null=True)
	result_id = models.ForeignKey('benchmarks.PgBenchStatement', on_delete=models.CASCADE)


class PgBenchStatement(models.Model):

	pgbench_statement_id = models.AutoField(primary_key=True)

	statement = models.TextField(null=True)