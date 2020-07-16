from django.db import models
from django.contrib.postgres.fields import ArrayField


class PgBenchBenchmark(models.Model):

	pgbench_benchmark_id = models.BigAutoField(primary_key=True)

	clients = models.IntegerField()
	scale = models.IntegerField()
	duration = models.FloatField()
	read_only = models.BooleanField()

	class Meta:
		unique_together = ('clients', 'scale', 'duration', 'read_only')


class PgBenchResult(models.Model):

	pgbench_result_id = models.AutoField(primary_key=True)

	run_id = models.ForeignKey('runs.RunInfo', related_name='pgbench_result', on_delete=models.CASCADE)

	benchmark_config = models.ForeignKey('benchmarks.PgBenchBenchmark', on_delete=models.CASCADE)

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