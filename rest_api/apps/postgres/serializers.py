import django_filters
import shortuuid
import json
import pandas
import hashlib
from rest_framework import serializers

from systems.models import LinuxInfo

# calculate the hash first
# see if it exists
# if so, just use pg_id for that run
# else, insert it and then populate the other table


class PostgresSettingsSetSerializer(serializers.ModelSerializer):

	settings_sha256 = serializers.SerializerMethodField()

    class Meta:
        model = PostgresSettingsSet
        fields = 'settings_sha256'

    def get_settings_sha256(self, obj):

        data_frame = pandas.DataFrame(data=obj)
        data_frame.query('source <> "default" and source <> "client"', inplace = True) 

        hash_string = data_frame.to_string()
        return hashlib.sha256(hash_string)


class PostgresSettingsSerializer(serializers.ModelSerializer, id):

    db_settings_id = serializers.SerializerMethodField(id)

    setting_name = serializers.SerializerMethodField()
    setting_unit = serializers.SerializerMethodField()
    setting_value = serializers.SerializerMethodField()

    def get_db_settings_id(self, obj, id):

        db_settings_id = PostgresSettingsSet.objects.filter(id=id).postgres_settings_set_id

        return db_settings_id

    def get_setting_name:
        pass

