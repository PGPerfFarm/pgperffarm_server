import django_filters
import shortuuid
import json
from rest_framework import serializers

from runs.models import RunInfo


class PgBenchBenchmarkSerializer(serializers.ModelSerializer):
