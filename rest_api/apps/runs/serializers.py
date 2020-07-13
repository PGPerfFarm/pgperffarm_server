import shortuuid
import json
from rest_framework import serializers

from runs.models import RunInfo, GitRepo
from benchmarks.serializers import PgBenchAllResultsSerializer
from systems.serializers import CompilerSerializer


class RunInfoSerializer(serializers.ModelSerializer):

	class Meta:
		model = RunInfo
		fields = '__all__'


class LastRunsSerializer(serializers.ModelSerializer):

	pgbench_result = PgBenchAllResultsSerializer(many=True, read_only=True)
	compiler = CompilerSerializer(read_only=True)

	class Meta:
	 	model = RunInfo
	 	fields = ['run_id', 'add_time', 'git_branch', 'git_commit', 'benchmark', 'machine_id', 'os_version', 'compiler', 'pgbench_result']


class GitRepoSerializer(serializers.ModelSerializer):

	class Meta:
		model = GitRepo
		fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):

	git_branch = serializers.CharField()
	results = serializers.IntegerField()
	latest = serializers.IntegerField()
	#commit = serializers.CharField()
	machines = serializers.IntegerField()


	class Meta:
		model = RunInfo
		#fields = ['git_branch', 'results', 'latest', 'commit', 'machines']
		fields = ['git_branch', 'results', 'machines']
