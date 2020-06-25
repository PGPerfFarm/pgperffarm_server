import shortuuid
import json
from rest_framework import serializers

from runs.models import RunInfo


class RunInfoSerializer(serializers.ModelSerializer):

	class Meta:
		model = RunInfo
		fields = '__all__'


