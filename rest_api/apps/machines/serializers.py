from rest_framework import serializers
from django.db.models import Count
from machines.models import Machine
from django.contrib.auth.models import User

from runs.serializers import LastRunsSerializer
from users.serializers import UserSerializer

# an automatically determined set of fields
# simple default implementations for the create() and update() methods

class MachineSerializer(serializers.ModelSerializer):

	alias = serializers.CharField()
	owner_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
	approved = serializers.ReadOnlyField()

	class Meta:
		model = Machine
		fields = ['machine_id','alias', 'add_time', 'approved', 'owner_id']


class MyMachineSerializer(serializers.ModelSerializer):

	class Meta:
		model = Machine
		fields = '__all__'


class MachineRunsSerializer(serializers.ModelSerializer):

	runs = LastRunsSerializer(many=True, read_only=True)
	owner = UserSerializer(read_only=True, source='owner_id')

	class Meta:
	 	model = Machine
	 	fields = ['machine_id','alias', 'add_time', 'approved', 'owner', 'runs', 'machine_type']