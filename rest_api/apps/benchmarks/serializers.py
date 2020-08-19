import json
from rest_framework import serializers

from benchmarks.models import PgBenchBenchmark, PgBenchResult, PgBenchStatement, PgBenchRunStatement, PgBenchLog
from runs.models import RunInfo, Branch
from runs.serializers import GitRepoSerializer, BranchSerializer, RunInfoSerializer
from systems.serializers import CompilerSerializer, OsDistVersionSerializer
from machines.serializers import MachineSerializer
from machines.models import Machine
from users.serializers import UserSerializer
from systems.serializers import OsKernelVersionSerializer, HardwareInfoSerializer
from postgres.serializers import PostgresSettingsSetSerializer


class PgBenchRunsSerializer(serializers.Serializer):

	run_id = serializers.IntegerField()
	pgbench_result_id = serializers.IntegerField()
	add_time = serializers.DateTimeField()


class PostgresHistorySerializer(serializers.Serializer):

	min = serializers.IntegerField()
	settings1 = serializers.IntegerField()
	settings2 = serializers.IntegerField() 
	setting_name = serializers.CharField()
	unit1 = serializers.CharField()
	unit2 = serializers.CharField()
	value1 = serializers.CharField()
	value2 = serializers.CharField()
	machine_id = serializers.IntegerField()
	add_time = serializers.DateTimeField()
	name = serializers.CharField()
	machine_type = serializers.CharField() 
	username = serializers.CharField()
	kernel_name = serializers.CharField()
	first_run = serializers.IntegerField()
	last_run = serializers.IntegerField()
	min_add_time = serializers.DateTimeField()
	max_add_time = serializers.DateTimeField()


class MachineHistorySerializer(serializers.Serializer):
	
	name = serializers.CharField()
	machine_id = serializers.IntegerField()
	count = serializers.IntegerField()
	description = serializers.CharField()
	alias = serializers.CharField()
	add_time = serializers.DateTimeField()
	machine_type = serializers.CharField()
	username = serializers.CharField()
	email = serializers.CharField()
	url = serializers.CharField()
	dist_name = serializers.CharField()
	kernel_name = serializers.CharField()
	kernel_release = serializers.CharField()
	kernel_version = serializers.CharField()
	release = serializers.CharField()
	codename = serializers.CharField()
	compiler = serializers.CharField()
	run_id = serializers.IntegerField()
	postgres_info_id = serializers.IntegerField()
	mounts = serializers.JSONField()
	sysctl = serializers.JSONField()
	hardware_info_id = serializers.IntegerField()
	pgbench_benchmark_id = serializers.IntegerField()
	scale = serializers.IntegerField()
	duration = serializers.IntegerField()
	read_only = serializers.BooleanField()
	clients = serializers.IntegerField()


class PgBenchTrendSerializer(serializers.Serializer):

	avgtps = serializers.FloatField()
	avglat = serializers.FloatField()
	stdtps = serializers.FloatField()
	stdlat = serializers.FloatField()
	mintps = serializers.FloatField()
	minlat = serializers.FloatField()
	maxtps = serializers.FloatField()
	maxlat = serializers.FloatField()
	git_commit = serializers.CharField()
	pgbench_benchmark_id = serializers.IntegerField()
	name = serializers.CharField()
	scale = serializers.IntegerField()
	duration = serializers.IntegerField()
	read_only = serializers.BooleanField()
	clients = serializers.IntegerField()
	machine_id = serializers.IntegerField()
	alias = serializers.CharField()
	machine_type = serializers.CharField()
	description = serializers.CharField()
	username = serializers.CharField()
	email = serializers.CharField()
	url = serializers.CharField()
	count = serializers.IntegerField()
	dist_name = serializers.CharField()
	kernel_name = serializers.CharField()
	compiler = serializers.CharField()


class PgBenchConfigMachineSerializer(serializers.Serializer):

	pgbench_benchmark_id = serializers.IntegerField()
	scale = serializers.IntegerField()
	duration = serializers.IntegerField()
	read_only = serializers.BooleanField()
	clients = serializers.IntegerField()
	machine_id = serializers.IntegerField()
	alias = serializers.CharField()
	add_time = serializers.DateTimeField()
	machine_type = serializers.CharField()
	username = serializers.CharField()
	count = serializers.IntegerField()
	description = serializers.CharField()


class RunBranchSerializer(serializers.ModelSerializer):

	git_repo = GitRepoSerializer(read_only=True)

	class Meta:
		model = Branch
		fields = ['branch_id', 'name', 'git_repo']


class PgBenchBenchmarkSerializer(serializers.ModelSerializer):

	class Meta:
		model = PgBenchBenchmark
		fields = '__all__'


class PgBenchResultSerializer(serializers.ModelSerializer):

	class Meta:
		model = PgBenchResult
		fields = '__all__'


class PgBenchStatementSerializer(serializers.ModelSerializer):

	class Meta:
		model = PgBenchStatement
		fields = '__all__'


class PgBenchRunSingleStatementSerializer(serializers.ModelSerializer):

	class Meta:
		model = PgBenchRunStatement
		fields = '__all__'


class PgBenchRunStatementSerializer(serializers.ModelSerializer):

	statements = PgBenchStatementSerializer(read_only=True, source="result_id")

	class Meta:
		model = PgBenchRunStatement
		fields = ['line_id', 'latency', 'statements']


class PgBenchLogSerializer(serializers.ModelSerializer):

	class Meta:
		model = PgBenchLog
		fields = '__all__'


class PgBenchAllResultsSerializer(serializers.ModelSerializer):

	benchmark_config = PgBenchBenchmarkSerializer(read_only=True)

	class Meta:
	 	model = PgBenchResult
	 	fields = ['pgbench_result_id', 'tps', 'latency', 'start', 'benchmark_config']


class LastRunsSerializer(serializers.ModelSerializer):

	pgbench_result = PgBenchAllResultsSerializer(many=True, read_only=True)
	compiler = CompilerSerializer(read_only=True)
	os_version = OsDistVersionSerializer(read_only=True, source='os_version_id')
	git_branch = RunBranchSerializer(read_only=True)

	class Meta:
	 	model = RunInfo
	 	fields = ['run_id', 'add_time', 'git_branch', 'git_commit', 'benchmark', 'os_version', 'os_kernel_version_id', 'compiler', 'git_branch', 'pgbench_result', 'postgres_info']


class MachineRunsSerializer(serializers.ModelSerializer):

	runs = serializers.SerializerMethodField()
	owner = UserSerializer(read_only=True, source='owner_id')

	class Meta:
	 	model = Machine
	 	fields = ['machine_id','alias', 'add_time', 'approved', 'owner', 'runs', 'machine_type']


	def get_runs(self, instance):
		runs = instance.runs.all().order_by('-add_time')
		return LastRunsSerializer(runs, many=True).data


class SingleRunSerializer(serializers.ModelSerializer):

	pgbench_result = PgBenchAllResultsSerializer(many=True, read_only=True)
	compiler = CompilerSerializer(read_only=True)
	os_version = OsDistVersionSerializer(read_only=True, source='os_version_id')
	git_branch = RunBranchSerializer(read_only=True)
	machine = MachineSerializer(source='machine_id', read_only=True)
	os_kernel = OsKernelVersionSerializer(source="os_kernel_version_id", read_only=True)
	hardware_info = HardwareInfoSerializer(read_only=True)
	postgres_info = PostgresSettingsSetSerializer(read_only=True)

	class Meta:
	 	model = RunInfo
	 	fields = ['run_id', 'add_time', 'git_branch', 'git_commit', 'os_version', 'os_kernel', 'compiler', 'git_branch', 'pgbench_result', 'postgres_info', 'machine', 'hardware_info']


class RunSerializer(serializers.ModelSerializer):

	compiler = CompilerSerializer(read_only=True)
	os_version = OsDistVersionSerializer(read_only=True, source='os_version_id')
	git_branch = RunBranchSerializer(read_only=True)
	machine = MachineSerializer(source='machine_id', read_only=True)
	os_kernel = OsKernelVersionSerializer(source="os_kernel_version_id", read_only=True)

	class Meta:
	 	model = RunInfo
	 	fields = ['run_id', 'add_time', 'git_branch', 'git_commit', 'os_version', 'os_kernel', 'compiler', 'git_branch', 'machine']


class PgBenchResultCompleteSerializer(serializers.ModelSerializer):

	benchmark_config = PgBenchBenchmarkSerializer(read_only=True)
	pgbench_run_statement = PgBenchRunStatementSerializer(read_only=True, many=True)
	pgbench_log = PgBenchLogSerializer(read_only=True, many=True)
	run = RunSerializer(read_only=True, source='run_id')


	class Meta:
	 	model = PgBenchResult
	 	fields = ['pgbench_result_id', 'tps', 'latency', 'mode', 'start', 'end', 'iteration', 'init', 'benchmark_config', 'pgbench_run_statement', 'pgbench_log', 'run']
	 	






