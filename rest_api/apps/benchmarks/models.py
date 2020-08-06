from django.db import models
from django.contrib.postgres.fields import ArrayField


class PgBenchBenchmark(models.Model):

	pgbench_benchmark_id = models.BigAutoField(primary_key=True)

	clients = models.IntegerField()
	scale = models.IntegerField()
	duration = models.IntegerField()
	read_only = models.BooleanField()

	class Meta:
		unique_together = ('clients', 'scale', 'duration', 'read_only')


class PgBenchResult(models.Model):

	pgbench_result_id = models.AutoField(primary_key=True)

	run_id = models.ForeignKey('runs.RunInfo', related_name='pgbench_result', on_delete=models.CASCADE)
	benchmark_config = models.ForeignKey('benchmarks.PgBenchBenchmark', on_delete=models.CASCADE, related_name='results')

	tps = models.FloatField()
	mode = models.CharField(max_length=100)
	latency = models.FloatField()
	start = models.FloatField()
	end = models.FloatField()
	iteration = models.IntegerField()
	init = models.FloatField()


class PgBenchRunStatement(models.Model):

	pgbench_run_statement_id = models.AutoField(primary_key=True)

	pgbench_result_id = models.ForeignKey('benchmarks.PgBenchResult', related_name='pgbench_run_statement', on_delete=models.CASCADE)
	line_id = models.IntegerField(null=True)
	latency = models.FloatField(null=True)
	result_id = models.ForeignKey('benchmarks.PgBenchStatement', on_delete=models.CASCADE)


class PgBenchStatement(models.Model):

	pgbench_statement_id = models.AutoField(primary_key=True)
	statement = models.TextField(null=True)


class PgBenchLog(models.Model):

	pgbench_log_id = models.AutoField(primary_key=True)
	pgbench_result_id = models.ForeignKey('benchmarks.PgBenchResult', on_delete=models.CASCADE, related_name='pgbench_log')

	interval_start = models.DateTimeField(null=True)
	num_transactions = models.IntegerField(null=True)
	sum_latency = models.BigIntegerField(null=True)
	sum_latency_2 = models.BigIntegerField(null=True)
	min_latency = models.IntegerField(null=True)
	max_latency= models.IntegerField(null=True)

