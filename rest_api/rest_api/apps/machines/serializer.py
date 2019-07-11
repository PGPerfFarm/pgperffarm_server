from rest_framework import serializers
from machines.models import Machine #, LANGUAGE_CHOICES, STYLE_CHOICES

class MachineSerializer(serializers.Serializer):

	id = serializers.IntegerField(read_only=True)
	alias = serializers.CharField(required=False, allow_blank=True, max_length=100)
	sn = serializers.CharField(style={'base_template': 'textarea.html'})
	os_name = serializers.CharField(max_length=100, default='')
	os_version = serializers.CharField(max_length=100, default='')
	comp_name = serializers.CharField(max_length=100, default='')
	comp_version = serializers.CharField(max_length=100, default='')
	reports = serializers.IntegerField(default=0)
	lastest = serializers.CharField(max_length=100, default='')
	state = serializers.CharField(max_length=10)

	def create(self, validated_data):
		"""
		Create and return a new `Machine` instance, given the validated data.
		"""
		return Machine.objects.create(**validated_data)

	def update(self, instance, validated_data):
		"""
		Update and return an existing `Machine` instance, given the validated data.
		"""
		instance.alias = validated_data.get('alias', instance.title)
		instance.sn = validated_data.get('sn', instance.title)
		instance.os_name = validated_data.get('os_name', instance.title)
		instance.os_version = validated_data.get('os_version', instance.title)
		instance.comp_name = validated_data.get('comp_name', instance.title)
		instance.comp_version = validated_data.get('comp_version', instance.title)
		instance.reports = validated_data.get('reports', instance.title)
		instance.lastest = validated_data.get('lastest', instance.title)
		instance.state = validated_data.get('state', instance.title)
		

		instance.save()
		return instance