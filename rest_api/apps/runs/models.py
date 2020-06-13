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

	run_id = models.AutoField(primary_key=True)

	machine_id = models.ForeignKey('machines.Machine', on_delete=models.CASCADE)

	add_time = models.DateTimeField(auto_now_add=True)

	os_type = models.CharField(max_length=1, blank=False, choices=os, default='L')

	os_name = models.CharField(max_length=100, blank=False)

	os_version = models.CharField(max_length=100, blank=False)

	os_config_info = models.ForeignKey('systems.LinuxInfo', on_delete=models.CASCADE)

	comp_name = models.CharField(max_length=100, blank=False)

	comp_version = models.CharField(max_length=100, blank=False)

	benchmark_id = models.ForeignKey('benchmarks.Benchmark', on_delete=models.CASCADE)

	#benchmark_result_id = models.ForeignKey('results.Result')

	git_branch = models.CharField(max_length=100, blank=False)

	git_commit = models.CharField(max_length=100, blank=False)

	run_received_time = models.DateTimeField()
	run_start_time = models.DateTimeField()
	run_end_time = models.DateTimeField()

	git_clone_log = models.TextField()
	git_clone_runtime = models.TimeField()

	configure_log = models.TextField()
	configure_runtime = models.TimeField()

	build_log = models.TextField()
	build_runtime = models.TimeField()

	install_log = models.TextField()
	install_runtime = models.TimeField()

	benchmark_log = models.TextField()
	benckmark = models.FloatField()

	cleanup_log = models.TextField()
	cleanup_runtime = models.TimeField()

	postgres_log = models.TextField()
	postgres_info = models.ForeignKey('postgres.PostgresSettingsSet', on_delete=models.CASCADE)
