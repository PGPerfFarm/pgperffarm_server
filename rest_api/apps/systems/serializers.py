import shortuuid
import json
from rest_framework import serializers

from systems.models import HardwareInfo, Compiler, KnownSysctlInfo, OsDistributor, Kernel, OsVersion, OsKernelVersion


class HardwareInfoSerializer(serializers.ModelSerializer):

	class Meta:
		model = HardwareInfo
		fields = '__all__'

	
class CompilerSerializer(serializers.ModelSerializer):

	class Meta:
		model = Compiler
		fields = '__all__'


class KnownSysctlInfoSerializer(serializers.ModelSerializer):

	class Meta:
		model = KnownSysctlInfo
		fields = '__all__'


class OsDistributorSerializer(serializers.ModelSerializer):

	class Meta:
		model = OsDistributor
		fields = '__all__'


class KernelSerializer(serializers.ModelSerializer):

	class Meta:
		model = Kernel
		fields = '__all__'


class OsVersionSerializer(serializers.ModelSerializer):

	class Meta:
		model = OsVersion
		fields = '__all__'


class OsKernelVersionSerializer(serializers.ModelSerializer):

	class Meta:
		model = OsKernelVersion
		fields = '__all__'