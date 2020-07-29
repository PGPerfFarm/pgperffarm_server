from rest_framework import serializers
from django.db.models import Count
from machines.models import Machine
from django.contrib.auth.models import User

from users.serializers import UserSerializer
from runs.models import RunInfo
from runs.serializers import RunInfoLatestSerializer

# an automatically determined set of fields
# simple default implementations for the create() and update() methods

class MachineSerializer(serializers.ModelSerializer):

	alias = serializers.CharField()
	owner = UserSerializer(read_only=True, source='owner_id')
	approved = serializers.ReadOnlyField()
	latest = serializers.SerializerMethodField()

	def update(self, instance, validated_data):
		instance.alias = validated_data.get('alias', instance.alias)
		instance.machine_type = validated_data.get('machine_type', instance.machine_type)
		instance.approved = validated_data.get('approved', instance.approved)
		return instance

	def get_latest(self, obj):
		run_info = RunInfo.objects.filter(machine_id=obj.machine_id).order_by('-add_time').first()
		serializer = RunInfoLatestSerializer(run_info)
		return serializer.data

	class Meta:
		model = Machine
		fields = ['machine_id','alias', 'add_time', 'approved', 'owner', 'machine_type', 'latest']


class MyMachineSerializer(serializers.ModelSerializer):

	class Meta:
		model = Machine
		fields = '__all__'
