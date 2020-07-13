from django.db import models
import shortuuid
import hashlib
from django.contrib.postgres.fields.jsonb import JSONField


class LinuxInfo(models.Model):

	# do not insert every time, only check if there are duplicates

	linux_info_id = models.AutoField(primary_key=True)

	cpu_brand = models.CharField(max_length=100, null=True)
	hz = models.CharField(max_length=100, null=True)
	cpu_cores = models.IntegerField(null=True)

	total_memory = models.BigIntegerField(null=True)
	mounts = JSONField(null=True)
	io = JSONField(null=True)

	sysctl = models.TextField(null=True)

	class Meta:
		unique_together = ('cpu_brand', 'cpu_cores', 'total_memory')


class Compiler(models.Model):

	compiler_id = models.AutoField(primary_key=True)
	compiler = models.CharField(max_length=200, null=False, unique=True)