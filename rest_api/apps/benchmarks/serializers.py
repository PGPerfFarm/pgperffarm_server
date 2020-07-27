import shortuuid
import json
from rest_framework import serializers

from benchmarks.models import PgBenchBenchmark, PgBenchResult, PgBenchStatement, PgBenchRunStatement, PgBenchLog
from runs.models import RunInfo
from runs.serializers import GitRepoSerializer, BranchSerializer
from systems.serializers import CompilerSerializer, OsVersionSerializer
from machines.serializers import MachineSerializer


class RunMachineSerializer(serializers.ModelSerializer):

	machine = MachineSerializer(read_only=True, source='machine_id')

	class Meta:
		model = RunInfo
		fields = ['machine']


class PgBenchBenchmarkSerializer(serializers.ModelSerializer):

	class Meta:
		model = PgBenchBenchmark
		fields = '__all__'


class PgBenchResultIdSerializer(serializers.ModelSerializer):

	run_id = RunMachineSerializer(read_only=True)

	class Meta:
		model = PgBenchResult
		fields = ['run_id']


class PgBenchBenchmarkMachineSerializer(serializers.ModelSerializer):

	results = PgBenchResultIdSerializer(read_only=True, many=True)

	class Meta:
		model = PgBenchBenchmark
		fields = ['pgbench_benchmark_id', 'scale', 'duration', 'read_only', 'clients', 'results']


class PgBenchResultSerializer(serializers.ModelSerializer):

	class Meta:
		model = PgBenchResult
		fields = '__all__'


class PgBenchStatementSerializer(serializers.ModelSerializer):

	class Meta:
		model = PgBenchStatement
		fields = '__all__'


class PgBenchRunStatementSerializer(serializers.ModelSerializer):

	class Meta:
		model = PgBenchRunStatement
		fields = '__all__'


class PgBenchLogSerializer(serializers.ModelSerializer):

	class Meta:
		model = PgBenchLog
		fields = '__all__'


class PgBenchAllResultsSerializer(serializers.ModelSerializer):

	benchmark_config = PgBenchBenchmarkSerializer(read_only=True)

	class Meta:
	 	model = PgBenchResult
	 	fields = ['tps', 'latency', 'benchmark_config']


class LastRunsSerializer(serializers.ModelSerializer):

	pgbench_result = PgBenchAllResultsSerializer(many=True, read_only=True)
	compiler = CompilerSerializer(read_only=True)
	os_version = OsVersionSerializer(read_only=True, source='os_version_id')
	git_repo = GitRepoSerializer(read_only=True)
	git_branch = BranchSerializer(read_only=True)

	class Meta:
	 	model = RunInfo
	 	fields = ['run_id', 'add_time', 'git_branch', 'git_commit', 'benchmark', 'os_version', 'os_kernel_version_id', 'compiler', 'git_repo', 'git_branch', 'pgbench_result', 'postgres_info']



