import shortuuid
import json
from rest_framework import serializers

from benchmarks.models import PgBenchBenchmark, PgBenchResult


class PgBenchBenchmarkSerializer(serializers.ModelSerializer):

	class Meta:
		model = PgBenchBenchmark
		fields = '__all__'


class PgBenchResultSerializer(serializers.ModelSerializer):

	class Meta:
		model = PgBenchResult
		fields = '__all__'
