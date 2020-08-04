import json
import pandas
import hashlib
from rest_framework import serializers

from postgres.models import PostgresSettingsSet, PostgresSettings

# calculate the hash first
# see if it exists
# if so, just use pg_id for that run
# else, insert it and then populate the other table

class PostgresSettingsSerializer(serializers.ModelSerializer):

	class Meta:
		model = PostgresSettings
		fields = '__all__'


class PostgresSettingsSetSerializer(serializers.ModelSerializer):

	settings_sha256 = serializers.CharField()
	settings = serializers.SerializerMethodField()

	class Meta:
		model = PostgresSettingsSet
		fields = ['postgres_settings_set_id', 'settings_sha256', 'settings']

	def get_settings(self, instance):
		settings = instance.settings.all().order_by('postgres_settings_id')
		return PostgresSettingsSerializer(settings, many=True).data





