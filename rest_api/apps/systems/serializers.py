import django_filters
import shortuuid
import json
from rest_framework import serializers

from systems.models import LinuxInfo


class LinuxInfoSerializer(serializers.ModelSerializer):

   	cpu_brand = serializers.SerializerMethodField()
	hz = serializers.SerializerMethodField()
	cpu_cores = serializers.SerializerMethodField()
	cpu_times = serializers.SerializerMethodField()

	memory = serializers.SerializerMethodField()
	swap = serializers.SerializerMethodField()
	mounts = serializers.SerializerMethodField()
	io = serializers.SerializerMethodField()

	sysctl = serializers.SerializerMethodField()

    class Meta:
        model = LinuxInfo
        fields = '__all__'

    def get_cpu_brand(self, obj):
        return obj.cpu.information.brand.__str__()

    def get_hz(self, obj):
        return obj.cpu.information.hz_actual.__str__()

    def get_cpu_cores(self, obj):
        return obj.cpu.information.count.__str__()

    def get_cpu_times(self, obj):
        return obj.cpu.times

    def get_memory(self, obj):
        return obj.memory.virtual

    def get_swap(self, obj):
        return obj.memory.swap

    def get_mounts(self, obj):
        return obj.memory.mounts

    def get_io(self, obj):
        return obj.disk.io

    def get_sysctl(self, obj):
        return obj.sysctl.__str__()