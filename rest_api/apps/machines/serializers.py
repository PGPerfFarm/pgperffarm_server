from rest_framework import serializers
from django.db.models import Count
from machines.models import Machine
from django.contrib.auth.models import User

from runs.models import RunInfo
from runs.serializers import RunInfoLatestSerializer
from users.serializers import UserSerializer

# an automatically determined set of fields
# simple default implementations for the create() and update() methods


class MachineSerializer(serializers.ModelSerializer):

	alias = serializers.CharField()
	owner = UserSerializer(read_only=True, source='owner_id')
	approved = serializers.ReadOnlyField()
	latest = serializers.SerializerMethodField()

	def get_latest(self, obj):
		run_info = RunInfo.objects.filter(machine_id=obj.machine_id).order_by('-add_time').first()
		serializer = RunInfoLatestSerializer(run_info)
		return serializer.data

	class Meta:
		model = Machine
		fields = ['machine_id','alias', 'add_time', 'approved', 'owner', 'machine_type', 'latest', 'count']


class MyMachineSerializer(serializers.ModelSerializer):

	latest = serializers.SerializerMethodField()
	count = serializers.SerializerMethodField()

	def get_latest(self, obj):
		run_info = RunInfo.objects.filter(machine_id=obj.machine_id).order_by('-add_time').first()
		serializer = RunInfoLatestSerializer(run_info)
		return serializer.data

	def get_count(self, obj):
		return obj.runs.count()

	class Meta:
		model = Machine
		fields = ['machine_id','alias', 'machine_secret', 'add_time', 'approved', 'machine_type', 'latest', 'count']


class MachineUserSerializer(serializers.ModelSerializer):

	machines = MyMachineSerializer(many=True, read_only=True)

	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'machines')
