from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core import validators
from rest_api.validators import ValidateDate


class PgBenchBenchmark(models.Model):

	pgbench_benchmark_id = models.BigAutoField(primary_key=True)

	clients = models.IntegerField(validators=[validators.MaxValueValidator(50), validators.MinValueValidator(1)])
	scale = models.IntegerField(validators=[validators.MaxValueValidator(1000), validators.MinValueValidator(1)])
	duration = models.IntegerField(validators=[validators.MaxValueValidator(10000), validators.MinValueValidator(1)])
	read_only = models.BooleanField()

	class Meta:
		unique_together = ('clients', 'scale', 'duration', 'read_only')


class PgBenchResult(models.Model):

	pgbench_result_id = models.AutoField(primary_key=True)

	run_id = models.ForeignKey('runs.RunInfo', related_name='pgbench_result', on_delete=models.CASCADE)
	benchmark_config = models.ForeignKey('benchmarks.PgBenchBenchmark', on_delete=models.CASCADE, related_name='results')

	tps = models.FloatField(validators=[validators.MaxValueValidator(100000000), validators.MinValueValidator(0)])
	mode = models.CharField(max_length=100)
	latency = models.FloatField(validators=[validators.MaxValueValidator(10000), validators.MinValueValidator(0)])
	start = models.FloatField()
	end = models.FloatField()
	iteration = models.IntegerField(validators=[validators.MinValueValidator(0)])
	init = models.FloatField(validators=[validators.MinValueValidator(0)])


class PgBenchRunStatement(models.Model):

	pgbench_run_statement_id = models.AutoField(primary_key=True)

	pgbench_result_id = models.ForeignKey('benchmarks.PgBenchResult', related_name='pgbench_run_statement', on_delete=models.CASCADE)
	line_id = models.IntegerField(null=True)
	latency = models.FloatField(null=True, validators=[validators.MaxValueValidator(1000), validators.MinValueValidator(0)])
	result_id = models.ForeignKey('benchmarks.PgBenchStatement', on_delete=models.CASCADE)


class PgBenchStatement(models.Model):

	pgbench_statement_id = models.AutoField(primary_key=True)
	statement = models.TextField(null=True, unique=True)


class PgBenchLog(models.Model):

	pgbench_log_id = models.AutoField(primary_key=True)
	pgbench_result_id = models.ForeignKey('benchmarks.PgBenchResult', on_delete=models.CASCADE, related_name='pgbench_log')

	interval_start = models.DateTimeField(null=True, validators=[ValidateDate])
	num_transactions = models.IntegerField(null=True, validators=[validators.MaxValueValidator(10000), validators.MinValueValidator(0)])
	sum_latency = models.BigIntegerField(null=True, validators=[validators.MaxValueValidator(1000000), validators.MinValueValidator(0)])
	sum_latency_2 = models.BigIntegerField(null=True, validators=[validators.MaxValueValidator(1000000), validators.MinValueValidator(0)])
	min_latency = models.IntegerField(null=True, validators=[validators.MaxValueValidator(100), validators.MinValueValidator(0)])
	max_latency= models.IntegerField(null=True, validators=[validators.MaxValueValidator(100), validators.MinValueValidator(0)])

