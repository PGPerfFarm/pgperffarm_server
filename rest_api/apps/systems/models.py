from django.db import models
import shortuuid
import hashlib
from django.contrib.postgres.fields.jsonb import JSONField


class LinuxInfo(models.Model):

	# do not insert every time, only check if there are duplicates

	linux_info_id = models.AutoField(primary_key=True)

	cpu_brand = models.CharField(max_length=100, null=True)
	hz = models.BigIntegerField(null=True)
	cpu_cores = models.IntegerField(null=True)

	total_memory = models.BigIntegerField(null=True)
	total_swap = models.BigIntegerField(null=True)

	mounts = JSONField(null=True)

	sysctl = models.TextField(null=True)

	class Meta:
		unique_together = ('cpu_brand', 'cpu_cores', 'total_memory')


class Compiler(models.Model):

	compiler_id = models.AutoField(primary_key=True)
	compiler = models.CharField(max_length=200, null=False, unique=True)


class KnownSysctlInfo(models.Model):

	# kernel parameters:
	# shmmax, shmmin, shmall, shmseg, shmmni, semmni, semmns, semmsl, semmap, semvmx

	# vm parameters:
	# nr_hugepages, nr_hugepages_mempolicy, nr_overcommit_hugepages, overcommit_kbytes, overcommit_memory, overcommit_ratio, swappiness, numa_stat , numa_zonelist_order, dirty_background_bytes, dirty_background_ratio, dirty_bytes, dirty_expire_centisecs, dirty_ratio, dirty_writeback_centisecs, dirtytime_expire_seconds

	os = (
		('L', 'Linux'), 
		('M', 'osX'), 
		('W', 'Windows'), 
		('B', 'FreeBsd')
		)

	sysctl_id = models.AutoField(primary_key=True)
	os = models.CharField(max_length=1, blank=False, choices=os, default='L')
	sysctl = JSONField(null=True, unique=True)
