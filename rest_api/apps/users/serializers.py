from django.contrib.auth.models import User
from rest_framework import serializers
from machines.models import Machine
from machines.serializers import MachineSerializer


class UserSerializer(serializers.ModelSerializer):
	machines = serializers.StringRelatedField(many=True, read_only=True)
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ('id', 'username', 'password', 'email', 'machines')


class TokenSerializer(serializers.Serializer):
	token = serializers.CharField(max_length=255)



