from django.db import models
import shortuuid
import hashlib


class Benchmark(models.Model):

	bench = (
		('PgBench', 'PgBench'),
		('TBD', 'Something else')
		)

	benchmark_type = models.CharField(max_length=10, blank=False, choices=bench)

	benchmark_config = models.BigIntegerField(blank=False)


class PgBenchBenchmark(models.Model):

	jobs = IntegerField()
	clients = IntegerField()
	length = IntegerField()
	init = IntegerField()
	warmup = IntegerField()
	runs = IntegerField()
	scale = IntegerField()
	duration = IntegerField()


class PgBenchResult(models.Model):

	tps = IntegerField()
	mode = IntegerField()
	threads = IntegerField()
	clients = IntegerField()
	latency = IntegerField()
	read_only = IntegerField()
	start = IntegerField()
	end = IntegerField()
	run = IntegerField()
