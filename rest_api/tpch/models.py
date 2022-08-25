from django.db import models
from django.core import validators


class TpchConfig(models.Model):
    id = models.BigAutoField(primary_key=True)
    scale_factor = models.FloatField(validators=[validators.MinValueValidator(0)])
    streams = models.IntegerField()

class TpchResult(models.Model):
    id = models.BigAutoField(primary_key=True)
    run_id = models.ForeignKey('runs.RunInfo', on_delete=models.CASCADE)
    benchmark_config = models.ForeignKey('tpch.TpchConfig', on_delete=models.CASCADE)
    power_score = models.FloatField(validators=[validators.MinValueValidator(0)])
    throughput_score = models.FloatField(validators=[validators.MinValueValidator(0)])
    composite_score = models.FloatField(validators=[validators.MinValueValidator(0)])  # QphH score


# model to store data for each query in the tpch query set executed during the run
class TpchQueryResult(models.Model):
    id = models.BigAutoField(primary_key=True)
    query_idx = models.SmallIntegerField()  # idx of the query in the dataset
    time = models.FloatField()  # execution time
    type = models.CharField(max_length=30)  # type of the query executed, like power, throughput, and refresh functions
    tpch_result = models.ForeignKey('tpch.TpchResult', on_delete=models.CASCADE)

