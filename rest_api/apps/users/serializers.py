from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
	machines = serializers.HyperlinkedRelatedField(
many=True, view_name='machine-detail', read_only=True)

	class Meta:
		model = User
		fields = ('url', 'id', 'username', 'machines')