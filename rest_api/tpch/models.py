from django.db import models
from django.core import validators

# Create your models here.
class Run(models.Model):
    run_id = models.BigAutoField(primary_key=True)
    date_submitted = models.DateTimeField()
    machine_id = models.ForeignKey('machines.Machine', on_delete=models.CASCADE, related_name='tpchrun')
    scale_factor = models.FloatField(validators=[validators.MinValueValidator(0)])
    QphH = models.FloatField(validators=[validators.MinValueValidator(0)])
