import django_filters
import shortuuid
import json
from rest_framework import serializers

from systems.models import LinuxInfo


class PostgresSettingsSetSerializer(serializers.ModelSerializer):

	sysctl = serializers.SerializerMethodField()

    class Meta:
        model = PostgresSettingsSet
        fields = '__all__'

    # ??????

