from django.db import models


# Create your models here.
class Run(models.Model):
    run_id = models.BigAutoField(primary_key=True)
    date_submitted = models.DateTimeField(auto_now_add=True)
    machine_id = models.ForeignKey('machines.Machine', on_delete=models.CASCADE, related_name='tpchrun')
    scale_factor = models.IntegerField(null=True)
    QphH = models.CharField(max_length=100)
