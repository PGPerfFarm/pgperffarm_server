from rest_framework import serializers
from django.db.models import Count
from machines.models import Machine
from django.contrib.auth.models import User

# an automatically determined set of fields
# simple default implementations for the create() and update() methods

class MachineSerializer(serializers.ModelSerializer):

	alias = serializers.CharField()
	owner_id = serializers.ReadOnlyField()
	approved = serializers.ReadOnlyField()

	class Meta:
		model = Machine
		fields = ['machine_id','alias', 'add_time', 'approved', 'owner_id']

class MyMachineSerializer(serializers.ModelSerializer):

	class Meta:
		model = Machine
		fields = '__all__'