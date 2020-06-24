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

	class Meta:
		model = PostgresSettings
		fields = '__all__'




