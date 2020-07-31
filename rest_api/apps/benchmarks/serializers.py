import shortuuid
import json
from rest_framework import serializers

from benchmarks.models import PgBenchBenchmark, PgBenchResult, PgBenchStatement, PgBenchRunStatement, PgBenchLog
from runs.models import RunInfo
from runs.serializers import GitRepoSerializer, BranchSerializer, RunInfoSerializer
from systems.serializers import CompilerSerializer, OsVersionSerializer
from machines.serializers import MachineSerializer
from machines.models import Machine
from users.serializers import UserSerializer
from systems.serializers import OsKernelVersionSerializer, HardwareInfoSerializer
from postgres.serializers import PostgresSettingsSetSerializer


class PgBenchTrendSerializer(serializers.Serializer):

	avgtps = serializers.FloatField()
	avglat = serializers.FloatField()
	stdtps = serializers.FloatField()
	stdlat = serializers.FloatField()
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
	username = serializers.CharField()
	url = serializers.CharField()


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
	 	fields = ['pgbench_result_id', 'tps', 'latency', 'benchmark_config']


class LastRunsSerializer(serializers.ModelSerializer):

	pgbench_result = PgBenchAllResultsSerializer(many=True, read_only=True)
	compiler = CompilerSerializer(read_only=True)
	os_version = OsVersionSerializer(read_only=True, source='os_version_id')
	git_repo = GitRepoSerializer(read_only=True)
	git_branch = BranchSerializer(read_only=True)

	class Meta:
	 	model = RunInfo
	 	fields = ['run_id', 'add_time', 'git_branch', 'git_commit', 'benchmark', 'os_version', 'os_kernel_version_id', 'compiler', 'git_repo', 'git_branch', 'pgbench_result', 'postgres_info']


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
	os_version = OsVersionSerializer(read_only=True, source='os_version_id')
	git_repo = GitRepoSerializer(read_only=True)
	git_branch = BranchSerializer(read_only=True)
	machine = MachineSerializer(source='machine_id', read_only=True)
	os_kernel = OsKernelVersionSerializer(source="os_kernel_version_id", read_only=True)
	hardware_info = HardwareInfoSerializer(read_only=True)
	postgres_info = PostgresSettingsSetSerializer(read_only=True)

	class Meta:
	 	model = RunInfo
	 	fields = ['run_id', 'add_time', 'git_branch', 'git_commit', 'os_version', 'os_kernel', 'compiler', 'git_repo', 'git_branch', 'pgbench_result', 'postgres_info', 'machine', 'hardware_info']


class RunSerializer(serializers.ModelSerializer):

	compiler = CompilerSerializer(read_only=True)
	os_version = OsVersionSerializer(read_only=True, source='os_version_id')
	git_repo = GitRepoSerializer(read_only=True)
	git_branch = BranchSerializer(read_only=True)
	machine = MachineSerializer(source='machine_id', read_only=True)
	os_kernel = OsKernelVersionSerializer(source="os_kernel_version_id", read_only=True)

	class Meta:
	 	model = RunInfo
	 	fields = ['run_id', 'add_time', 'git_branch', 'git_commit', 'os_version', 'os_kernel', 'compiler', 'git_repo', 'git_branch', 'machine']


class PgBenchResultCompleteSerializer(serializers.ModelSerializer):

	benchmark_config = PgBenchBenchmarkSerializer(read_only=True)
	pgbench_run_statement = PgBenchRunStatementSerializer(read_only=True, many=True)
	pgbench_log = PgBenchLogSerializer(read_only=True, many=True)
	run = RunSerializer(read_only=True, source='run_id')


	class Meta:
	 	model = PgBenchResult
	 	fields = ['pgbench_result_id', 'tps', 'latency', 'mode', 'start', 'end', 'iteration', 'init', 'benchmark_config', 'pgbench_run_statement', 'pgbench_log', 'run']
	 	






