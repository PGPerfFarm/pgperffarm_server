from datetime import datetime
from django.db import models

from users.models import UserMachine
from test.models import Test, TestBranch

# Create your models here.


class TestResult(models.Model):
    """
    test result sample:

    "latency": -1,
    "scale": "10",
    "end": 1526184453.133798,
    "clients": "2",
    "start": 1526184333.102856,
    "run": 0,
    "threads": "2",
    "mode": "simple",
    "duration": "120",
    "tps": "369.666116",
    "read-only": false

    """

    test_item = models.ForeignKey(Test, verbose_name="test item", help_text="test item")
    latency = models.IntegerField(verbose_name="latency", help_text="latency of the test result")
    scale = models.IntegerField(verbose_name="scale", help_text="scale of the test result")
    end = models.DecimalField(max_digits=16, decimal_places=6, verbose_name="end",
                              help_text="endtime of the test result")
    clients = models.IntegerField(verbose_name="clients", help_text="clients of the test result")
    start = models.DecimalField(max_digits=16, decimal_places=6, verbose_name="start",
                                help_text="starttime of the test result")
    run = models.IntegerField(verbose_name="run", help_text="run number")
    threads = models.IntegerField(verbose_name="threads", help_text="threads of the test result")

    MODE_CHOICE = (
        ('1', 'simple'),
    )
    mode = models.IntegerField(choices=MODE_CHOICE, verbose_name="mode", help_text="test mode")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="test result added time")

    class Meta:
        verbose_name = "test result"
        verbose_name_plural = "test result"
