from django.db import models
import shortuuid
import hashlib


class RunInfo(models.Model):

	os = (
		('L', 'Linux'), 
		('M', 'osX'), 
		('W', 'Windows'), 
		('B', 'FreeBsd')
		)

	# run_id is implicit and auto incrementing by default

	run_id = models.BigAutoField(primary_key=True)

	machine_id = models.ForeignKey('machines.Machine', on_delete=models.CASCADE)

	add_time = models.DateTimeField(auto_now_add=True)

	os_type = models.CharField(max_length=1, blank=False, choices=os, default='L')

	os_name = models.CharField(max_length=100, blank=False)

	os_version = models.CharField(max_length=100, blank=False)

	os_config_info = models.ForeignKey('systems.LinuxInfo', on_delete=models.CASCADE)

	compiler = models.ForeignKey('systems.Compiler', on_delete=models.CASCADE)

	git_branch = models.CharField(max_length=100, blank=False)

	git_commit = models.CharField(max_length=100, blank=False)

	run_received_time = models.DateTimeField(null=True, blank=True)
	run_start_time = models.DateTimeField(null=True, blank=True)
	run_end_time = models.DateTimeField(null=True, blank=True)

	git_clone_log = models.TextField(null=True, blank=True)
	git_clone_runtime = models.DurationField(null=True, blank=True)
	git_pull_runtime = models.DurationField(null=True, blank=True)

	configure_log = models.TextField(null=True, blank=True)
	configure_runtime = models.DurationField(null=True, blank=True)

	build_log = models.TextField(null=True, blank=True)
	build_runtime = models.DurationField(null=True, blank=True)

	install_log = models.TextField(null=True, blank=True)
	install_runtime = models.DurationField(null=True, blank=True)

	benchmark_log = models.TextField(null=True, blank=True)
	benchmark = models.CharField(max_length=100)

	cleanup_log = models.TextField(null=True, blank=True)
	cleanup_runtime = models.DurationField(null=True, blank=True)

	postgres_log = models.TextField(null=True, blank=True)
	postgres_info = models.ForeignKey('postgres.PostgresSettingsSet', on_delete=models.CASCADE)


	class Meta:
		unique_together = ('machine_id', 'run_start_time')
