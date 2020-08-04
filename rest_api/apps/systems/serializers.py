import json
from rest_framework import serializers

from systems.models import HardwareInfo, Compiler, OsDistributor, Kernel, OsVersion, OsKernelVersion


class HardwareInfoSerializer(serializers.ModelSerializer):

	class Meta:
		model = HardwareInfo
		fields = '__all__'

	
class CompilerSerializer(serializers.ModelSerializer):

	class Meta:
		model = Compiler
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

	dist = OsDistributorSerializer(read_only=True, source='dist_id')

	class Meta:
		model = OsVersion
		fields = ['os_version_id', 'dist', 'description', 'release', 'codename']


class OsKernelVersionSerializer(serializers.ModelSerializer):

	kernel = KernelSerializer(read_only=True, source='kernel_id')

	class Meta:
		model = OsKernelVersion
		fields = ['os_kernel_version_id', 'kernel_id', 'kernel_release', 'kernel_version', 'kernel']