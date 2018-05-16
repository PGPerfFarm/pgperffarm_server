from datetime import datetime
from django.db import models
from tests.models import Tests,TestBranch
from users.models import UserProfile

# Create your models here.

class UserMachine(models.Model):
    """
    user machine
    """
    machine_sn = models.CharField(max_length=16, verbose_name="machine sn")
    machine_secret = models.CharField(max_length=32, verbose_name="machine secret")
    machine_owner = models.ForeignKey(UserProfile)
    alias = models.CharField(max_length=16, verbose_name="alias")
    os_name = models.CharField(max_length=32, verbose_name="operation system name")
    os_version = models.CharField(max_length=32, verbose_name="operation system version")
    comp_name = models.CharField(max_length=32, verbose_name="compiler name")
    comp_version = models.CharField(max_length=32, verbose_name="compiler version")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="machine added time")

    class Meta:
        verbose_name = "user machines"
        verbose_name_plural = "user machines"

    def __str__(self):
        return self.machine_sn

class TestResult(models.Model):
    """
    test result
    """
    test = models.ForeignKey(Tests)
    machine = models.ForeignKey(UserMachine)
    pg_config = models.TextField(verbose_name="postgresql config", help_text="postgresql config")
    os_config = models.TextField(verbose_name="os config", help_text="os config")
    result_desc = models.TextField(verbose_name="test result", help_text="test result")
    test_branch = models.ForeignKey(TestBranch, verbose_name="test branch", help_text="branch of this test")

    test_time = models.DateTimeField(verbose_name="test time")

    class Meta:
        verbose_name = "test result"
        verbose_name_plural = "test result"

