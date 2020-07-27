from rest_framework import serializers
from django.db.models import Count
from machines.models import Machine
from django.contrib.auth.models import User

from users.serializers import UserSerializer

# an automatically determined set of fields
# simple default implementations for the create() and update() methods

class MachineSerializer(serializers.ModelSerializer):

	alias = serializers.CharField()
	owner = UserSerializer(read_only=True, source='owner_id')
	approved = serializers.ReadOnlyField()

	def update(self, instance, validated_data):
		instance.alias = validated_data.get('alias', instance.alias)
		instance.machine_type = validated_data.get('machine_type', instance.machine_type)
		instance.approved = validated_data.get('approved', instance.approved)
		return instance

	class Meta:
		model = Machine
		fields = ['machine_id','alias', 'add_time', 'approved', 'owner', 'machine_type']


class MyMachineSerializer(serializers.ModelSerializer):

	class Meta:
		model = Machine
		fields = '__all__'


class MachineRunsSerializer(serializers.ModelSerializer):

	runs = serializers.SerializerMethodField()
	owner = UserSerializer(read_only=True, source='owner_id')

	class Meta:
	 	model = Machine
	 	fields = ['machine_id','alias', 'add_time', 'approved', 'owner', 'runs', 'machine_type']


	def get_runs(self, instance):
		runs = instance.runs.all().order_by('-add_time')
		return LastRunsSerializer(runs, many=True).data
