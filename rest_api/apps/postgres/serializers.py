import shortuuid
import json
import pandas
import hashlib
from rest_framework import serializers

from postgres.models import PostgresSettingsSet, PostgresSettings

# calculate the hash first
# see if it exists
# if so, just use pg_id for that run
# else, insert it and then populate the other table


class PostgresSettingsSetSerializer(serializers.ModelSerializer):

	settings_sha256 = serializers.CharField()

	class Meta:
		model = PostgresSettingsSet
		fields = '__all__'


class PostgresSettingsSerializer(serializers.ModelSerializer):

	db_settings_id = serializers.SerializerMethodField(id)

	setting_name = serializers.SerializerMethodField()
	setting_unit = serializers.SerializerMethodField()
	setting_value = serializers.SerializerMethodField()

	def get_db_settings_id(self, obj, id):

		db_settings_id = PostgresSettingsSet.objects.filter(id=id).postgres_settings_set_id

		return db_settings_id



