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

	#comp_name = models.CharField(max_length=100, blank=False)

	compiler = models.ForeignKey('systems.Compiler', on_delete=models.CASCADE)

	git_branch = models.CharField(max_length=100, blank=False)

	git_commit = models.CharField(max_length=100, blank=False)

	run_received_time = models.DateTimeField(null=True)
	run_start_time = models.DateTimeField(null=True)
	run_end_time = models.DateTimeField(null=True)

	git_clone_log = models.TextField(null=True)
	git_clone_runtime = models.TimeField(null=True)

	configure_log = models.TextField(null=True)
	configure_runtime = models.FloatField(null=True)

	build_log = models.TextField(null=True)
	build_runtime = models.FloatField(null=True)

	install_log = models.TextField(null=True)
	install_runtime = models.FloatField(null=True)

	benchmark_log = models.TextField(null=True)
	benckmark = models.CharField(max_length=100)

	cleanup_log = models.TextField(null=True)
	cleanup_runtime = models.FloatField(null=True)

	postgres_log = models.TextField(null=True)
	postgres_info = models.ForeignKey('postgres.PostgresSettingsSet', on_delete=models.CASCADE)
