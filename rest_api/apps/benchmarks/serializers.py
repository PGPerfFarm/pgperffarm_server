import shortuuid
import json
from rest_framework import serializers

from benchmarks.models import PgBenchBenchmark, PgBenchResult, PgBenchStatement, PgBenchRunStatement


class PgBenchBenchmarkSerializer(serializers.ModelSerializer):

	class Meta:
		model = PgBenchBenchmark
		fields = '__all__'


class PgBenchResultSerializer(serializers.ModelSerializer):

	class Meta:
		model = PgBenchResult
		fields = '__all__'


class PgBenchStatementSerializer(serializers.ModelSerializer):

	class Meta:
		model = PgBenchStatement
		fields = '__all__'


class PgBenchRunStatementSerializer(serializers.ModelSerializer):

	class Meta:
		model = PgBenchRunStatement
		fields = '__all__'


class PgBenchAllResultsSerializer(serializers.ModelSerializer):

	#pgbench_run_statement = PgBenchRunStatementSerializer(many=True, read_only=True)

	class Meta:
	 	model = PgBenchResult
	 	fields = ['tps', 'threads', 'latency', 'read_only', 'benchmark_config']
