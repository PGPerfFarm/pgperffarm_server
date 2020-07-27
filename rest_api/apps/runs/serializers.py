import shortuuid
import json
from rest_framework import serializers

from runs.models import RunInfo, GitRepo, Branch
from benchmarks.serializers import PgBenchAllResultsSerializer
from systems.serializers import CompilerSerializer, OsVersionSerializer


class RunInfoSerializer(serializers.ModelSerializer):

	class Meta:
		model = RunInfo
		fields = '__all__'


class GitRepoSerializer(serializers.ModelSerializer):

	class Meta:
		model = GitRepo
		fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):

	class Meta:
		model = Branch
		fields = '__all__'
		

class LastRunsSerializer(serializers.ModelSerializer):

	pgbench_result = PgBenchAllResultsSerializer(many=True, read_only=True)
	compiler = CompilerSerializer(read_only=True)
	os_version = OsVersionSerializer(read_only=True, source='os_version_id')
	git_repo = GitRepoSerializer(read_only=True)
	git_branch = BranchSerializer(read_only=True)

	class Meta:
	 	model = RunInfo
	 	fields = ['run_id', 'add_time', 'git_branch', 'git_commit', 'benchmark', 'os_version', 'os_kernel_version_id', 'compiler', 'git_repo', 'git_branch', 'pgbench_result', 'postgres_info']


