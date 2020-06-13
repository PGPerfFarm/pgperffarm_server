from django.db import models
import shortuuid
import hashlib


class Benchmark(models.Model):

	benchmark_id = models.AutoField(primary_key=True)

	bench = (
		('PgBench', 'PgBench'),
		('TBD', 'Something else')
		)

	benchmark_type = models.CharField(max_length=10, blank=False, choices=bench)

	benchmark_config = models.BigIntegerField(blank=False)


class PgBenchBenchmark(models.Model):

	pgbench_benchmark_id = models.AutoField(primary_key=True)

	jobs = models.IntegerField()
	clients = models.IntegerField()
	length = models.IntegerField()
	init = models.IntegerField()
	warmup = models.IntegerField()
	runs = models.IntegerField()
	scale = models.IntegerField()
	duration = models.IntegerField()


class PgBenchResult(models.Model):

	pgbench_result_id = models.AutoField(primary_key=True)

	tps = models.IntegerField()
	mode = models.IntegerField()
	threads = models.IntegerField()
	clients = models.IntegerField()
	latency = models.FloatField()
	read_only = models.BooleanField()
	start = models.IntegerField()
	end = models.IntegerField()
	run = models.IntegerField()


class PgBenchRunStatement(models.Model):

	pgbench_run_statement_id = models.AutoField(primary_key=True)

	run_id = models.ForeignKey('runs.RunInfo', on_delete=models.CASCADE)
	line_id = models.IntegerField()
	latency = models.FloatField()


class PgBenchStatement(models.Model):

	pgbench_statement_id = models.AutoField(primary_key=True)

	statement = models.TextField()