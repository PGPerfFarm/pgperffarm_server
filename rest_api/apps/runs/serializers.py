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

