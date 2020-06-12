from django.db import models
import shortuuid
import hashlib


class LinuxInfo(models.Model):

	linux_info_id = models.AutoField(primary_key=True)

	mounts = models.TextField()
	cpuinfo = models.TextField()
	sysctl = models.TextField()
	meminfo = models.TextField()