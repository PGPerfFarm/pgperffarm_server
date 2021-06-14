from django.db import models
from django.contrib.postgres.fields.jsonb import JSONField
from django.contrib.postgres.fields import ArrayField
from django.core import validators


class HardwareInfo(models.Model):

    # do not insert every time, only check if there are duplicates

    hardware_info_id = models.AutoField(primary_key=True)

    cpu_brand = models.CharField(max_length=100, null=True)
    hz = models.BigIntegerField(null=True, validators=[validators.MaxValueValidator(10000000), validators.MinValueValidator(0)])
    cpu_cores = models.IntegerField(null=True, validators=[validators.MaxValueValidator(1000), validators.MinValueValidator(0)])

    total_memory = models.BigIntegerField(null=True, validators=[validators.MaxValueValidator(10000000000), validators.MinValueValidator(0)])
    total_swap = models.BigIntegerField(null=True, validators=[validators.MaxValueValidator(1000000000), validators.MinValueValidator(0)])

    mounts = JSONField(null=True)
    mounts_hash = models.CharField(max_length=256, null=False)

    sysctl = JSONField(null=True)
    sysctl_hash = models.CharField(max_length=256, null=False)

    class Meta:
        unique_together = ('cpu_brand', 'hz', 'cpu_cores', 'total_memory', 'total_swap', 'mounts_hash', 'sysctl_hash')


class Compiler(models.Model):

    compiler_id = models.AutoField(primary_key=True)
    compiler = models.CharField(max_length=200, null=False, unique=True)


class OsDistributor(models.Model):

    os_distributor_id = models.AutoField(primary_key=True)
    dist_name = models.CharField(max_length=100, null=False, unique=True)


class Kernel(models.Model):

    kernel_id = models.AutoField(primary_key=True)
    kernel_name = models.CharField(max_length=100, null=False, unique=True)
    sysctl = ArrayField(models.CharField(max_length=50, null=True, unique=True))

    class Meta:
        unique_together = ('kernel_name', 'sysctl')


class OsKernelVersion(models.Model):

    os_kernel_version_id = models.AutoField(primary_key=True)
    kernel_id = models.ForeignKey('systems.Kernel', on_delete=models.CASCADE, related_name='distributor')
    kernel_release = models.CharField(max_length=100, null=True)
    kernel_version = models.CharField(max_length=100, null=True)

    class Meta:
        unique_together = ('kernel_id', 'kernel_release', 'kernel_version')


class OsVersion(models.Model):

    os_version_id = models.AutoField(primary_key=True)
    dist_id = models.ForeignKey('systems.OsDistributor', on_delete=models.CASCADE, related_name='distributor')

    description = models.CharField(max_length=100, null=True)
    release = models.CharField(max_length=100, null=True)
    codename = models.CharField(max_length=100, null=True)

    class Meta:
        unique_together = ('dist_id', 'description', 'release', 'codename')
