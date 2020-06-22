import shortuuid
import json
from rest_framework import serializers

from systems.models import LinuxInfo, Compiler


class LinuxInfoSerializer(serializers.ModelSerializer):

	cpu_brand = serializers.CharField()

	hz = serializers.CharField()
	cpu_cores = serializers.IntegerField()
	cpu_times = serializers.JSONField()

	memory = serializers.JSONField()
	swap = serializers.JSONField()


	class Meta:
		model = LinuxInfo
		fields = ['cpu_brand', 'hz', 'cpu_cores', 'cpu_times', 'memory', 'swap']

	
class CompilerSerializer(serializers.ModelSerializer):

	class Meta:
		model = Compiler
		fields = '__all__'