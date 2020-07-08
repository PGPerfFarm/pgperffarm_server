import shortuuid
import json
from rest_framework import serializers

from runs.models import RunInfo, GitRepo


class RunInfoSerializer(serializers.ModelSerializer):

	class Meta:
		model = RunInfo
		fields = '__all__'


class GitRepoSerializer(serializers.ModelSerializer):

	class Meta:
		model = GitRepo
		fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):

	git_branch = serializers.CharField()
	results = serializers.IntegerField()
	#latest = serializers.IntegerField()
	#commit = serializers.CharField()
	machines = serializers.IntegerField()


	class Meta:
		model = RunInfo
		#fields = ['git_branch', 'results', 'latest', 'commit', 'machines']
		fields = ['git_branch', 'results', 'machines']
