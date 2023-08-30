from django.db import models
from django.core import validators
from django.db.models import JSONField


class TpchConfig(models.Model):
    id = models.BigAutoField(primary_key=True)
    scale_factor = models.FloatField(
        validators=[validators.MinValueValidator(0)])
    streams = models.IntegerField()


class TpchResult(models.Model):
    id = models.BigAutoField(primary_key=True)
    run_id = models.ForeignKey('runs.RunInfo', on_delete=models.CASCADE)
    benchmark_config = models.ForeignKey(
        'tpch.TpchConfig', on_delete=models.CASCADE)
    power_score = models.FloatField(
        validators=[validators.MinValueValidator(0)])
    throughput_score = models.FloatField(
        validators=[validators.MinValueValidator(0)])
    composite_score = models.FloatField(
        validators=[validators.MinValueValidator(0)])  # QphH score


# model to store data for each query in the tpch query set executed during the run
class TpchQueryResult(models.Model):
    id = models.BigAutoField(primary_key=True)
    query_idx = models.SmallIntegerField(
        default=1)  # idx of the query in the dataset
    time = models.FloatField()  # execution time
    # type of the query executed, like power, throughput, and refresh functions
    type = models.CharField(max_length=30)
    tpch_result = models.ForeignKey(
        'tpch.TpchResult', on_delete=models.CASCADE)

    query_id = models.ForeignKey(
        'tpch.TpchQuery', on_delete=models.CASCADE, default=None)


#  New Models


# model to store the explain query cost on result


class TpchQuery(models.Model):
    query_id = models.SmallIntegerField(primary_key=True, default=1)
    query_statement = models.CharField(max_length=2000, default=None)


class ExplainQueryCostOnResult(models.Model):
    tpch_query = models.ForeignKey('tpch.TpchQuery', on_delete=models.CASCADE)
    tpch_result = models.ForeignKey(
        'tpch.TpchResult', on_delete=models.CASCADE)
    planning_time = models.FloatField()
    execution_time = models.FloatField()


class ExplainQueryCostOnResultDetails(models.Model):
    explain_query_cost_on_result = models.ForeignKey(
        'tpch.ExplainQueryCostOnResult', on_delete=models.CASCADE)
    result = JSONField()


# we need store the explain query cost off result only ones

class ExplainQueryCostOffPlan(models.Model):
    hash = models.CharField(primary_key=True, max_length=64)
    result = JSONField(default=None)


class ExplainQueryCostOffResult(models.Model):
    tpch_query = models.ForeignKey(
        'tpch.TpchQueryResult', on_delete=models.CASCADE)
    plan_hash = models.ForeignKey(
        'tpch.ExplainQueryCostOffPlan', on_delete=models.CASCADE, default=None)
