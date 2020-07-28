from django.db import models
import shortuuid
import hashlib
from django.contrib.postgres.fields.jsonb import JSONField


class GitRepo(models.Model):

	git_repo_id = models.BigAutoField(primary_key=True)
	url = models.CharField(max_length=100)
	owner = models.CharField(max_length=100, null=True, blank=True)

	'''
	class Meta:
		unique_together = ('url', 'author')
	'''


class Branch(models.Model):

	branch_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	default_view = models.BooleanField(default=False)
	ordering = models.IntegerField(null=True)
	git_repo = models.ForeignKey('runs.GitRepo', on_delete=models.CASCADE)

	class Meta:
		unique_together = ('name', 'git_repo')


class RunInfo(models.Model):

	run_id = models.BigAutoField(primary_key=True)

	machine_id = models.ForeignKey('machines.Machine', on_delete=models.CASCADE, related_name='runs')

	add_time = models.DateTimeField(auto_now_add=True)

	os_version_id = models.ForeignKey('systems.OsVersion', on_delete=models.CASCADE)
	os_kernel_version_id = models.ForeignKey('systems.OsKernelVersion', on_delete=models.CASCADE)
	hardware_info = models.ForeignKey('systems.HardwareInfo', on_delete=models.CASCADE)
	
	#sysctl_info = models.ForeignKey('systems.KnownSysctlInfo', on_delete=models.CASCADE)

	sysctl_raw = JSONField(null=True)

	compiler = models.ForeignKey('systems.Compiler', on_delete=models.CASCADE)

	git_branch = models.ForeignKey('runs.Branch', on_delete=models.CASCADE)
	git_commit = models.CharField(max_length=100, blank=False)

	run_received_time = models.DateTimeField(null=True, blank=True)
	run_start_time = models.DateTimeField(null=True, blank=True)
	run_end_time = models.DateTimeField(null=True, blank=True)

	git_clone_log = models.TextField(null=True, blank=True)
	git_clone_runtime = models.DurationField(null=True, blank=True)
	git_pull_runtime = models.DurationField(null=True, blank=True)
	git_repo = models.ForeignKey('runs.GitRepo', on_delete=models.CASCADE)

	configure_log = models.TextField(null=True, blank=True)
	configure_runtime = models.DurationField(null=True, blank=True)

	build_log = models.TextField(null=True, blank=True)
	build_runtime = models.DurationField(null=True, blank=True)

	install_log = models.TextField(null=True, blank=True)
	install_runtime = models.DurationField(null=True, blank=True)

	benchmark_log = models.TextField(null=True, blank=True)
	benchmark = models.CharField(max_length=100, default="pgbench")

	cleanup_log = models.TextField(null=True, blank=True)
	cleanup_runtime = models.DurationField(null=True, blank=True)

	postgres_log = models.TextField(null=True, blank=True)
	postgres_info = models.ForeignKey('postgres.PostgresSettingsSet', on_delete=models.CASCADE)


	class Meta:
		unique_together = ('machine_id', 'run_start_time')


