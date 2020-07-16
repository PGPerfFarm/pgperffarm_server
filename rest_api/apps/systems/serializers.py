import shortuuid
import json
from rest_framework import serializers

from systems.models import LinuxInfo, Compiler, KnownSysctlInfo


class LinuxInfoSerializer(serializers.ModelSerializer):

	class Meta:
		model = LinuxInfo
		fields = ['cpu_brand', 'hz', 'cpu_cores', 'total_memory', 'total_swap']

	
class CompilerSerializer(serializers.ModelSerializer):

	class Meta:
		model = Compiler
		fields = '__all__'


class KnownSysctlInfoSerializer(serializers.ModelSerializer):

	class Meta:
		model = KnownSysctlInfo
		fields = '__all__'