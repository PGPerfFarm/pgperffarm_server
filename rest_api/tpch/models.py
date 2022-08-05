from django.db import models
from django.core import validators


# model to store infos about each run of tpch
class Run(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_submitted = models.DateTimeField()
    machine = models.ForeignKey('machines.Machine', on_delete=models.CASCADE, related_name='tpch_run')
    git_commit = models.CharField(max_length=100, blank=False)
    git_branch = models.ForeignKey('runs.Branch', on_delete=models.CASCADE)
    scale_factor = models.FloatField(validators=[validators.MinValueValidator(0)])
    power_score = models.FloatField(validators=[validators.MinValueValidator(0)])
    throughput_score = models.FloatField(validators=[validators.MinValueValidator(0)])
    composite_score = models.FloatField(validators=[validators.MinValueValidator(0)])  # QphH score


# model to store data for each query in the tpch query set executed during the run
class QueryResult(models.Model):
    id = models.BigAutoField(primary_key=True)
    query_idx = models.SmallIntegerField()  # idx of the query in the dataset
    time = models.FloatField()  # execution time
    type = models.CharField(max_length=30)  # type of the query executed, like power, throughput, and refresh functions
    run = models.ForeignKey('tpch.Run', on_delete=models.CASCADE, related_name='tpch_queryresult')

