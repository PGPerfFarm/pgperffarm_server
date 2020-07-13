import shortuuid
import json
from rest_framework import serializers

from systems.models import LinuxInfo, Compiler


class LinuxInfoSerializer(serializers.ModelSerializer):

	class Meta:
		model = LinuxInfo
		fields = ['cpu_brand', 'hz', 'cpu_cores', 'total_memory']

	
class CompilerSerializer(serializers.ModelSerializer):

	class Meta:
		model = Compiler
		fields = '__all__'