import json
from rest_framework import serializers

from runs.models import RunInfo, GitRepo, Branch, RunLog


class RunInfoSerializer(serializers.ModelSerializer):

	class Meta:
		model = RunInfo
		fields = '__all__'


class RunLogSerializer(serializers.ModelSerializer):

	class Meta:
		model = RunLog
		fields = '__all__'


class RunInfoLatestSerializer(serializers.ModelSerializer):

	class Meta:
		model = RunInfo
		fields = ['run_id']


class GitRepoSerializer(serializers.ModelSerializer):

	class Meta:
		model = GitRepo
		fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):

	class Meta:
		model = Branch
		fields = '__all__'





