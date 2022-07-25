from django.db import models
from django.core import validators

# Create your models here.
class Run(models.Model):
    run_id = models.BigAutoField(primary_key=True)
    date_submitted = models.DateTimeField()
    machine = models.ForeignKey('machines.Machine', on_delete=models.CASCADE, related_name='tpch_run')
    scale_factor = models.FloatField(validators=[validators.MinValueValidator(0)])
    qphh = models.FloatField(validators=[validators.MinValueValidator(0)])
