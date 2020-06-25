import pandas
import csv
import json
import hashlib
import io
import re

from postgres.models import PostgresSettingsSet
from postgres.serializers import PostgresSettingsSerializer
from benchmarks.serializers import PgBenchResultSerializer

def ParseLinuxData(json_data):

	result = {
		'cpu_brand': json_data['linux']['cpu']['information']['brand'],
		'hz': json_data['linux']['cpu']['information']['hz_actual'],
		'cpu_cores': json_data['linux']['cpu']['information']['count'],
		'cpu_times': json_data['linux']['cpu']['times'],
		'memory': json_data['linux']['memory']['virtual'],
		'swap': json_data['linux']['memory']['swap'],
		'mounts': json_data['linux']['memory']['mounts'],
		'io': json_data['linux']['disk']['io'],
		'sysctl': json_data['sysctl_log']
	}

	return result


def GetHash(postgres_settings):

	reader = csv.DictReader(io.StringIO(postgres_settings))
	postgres_settings_json = json.dumps(list(reader))

	data_frame = pandas.read_json(postgres_settings_json)

	data_frame.query('source != "default" and source != "client"', inplace = True)

	hash_string = str(data_frame.values.flatten())

	hash_value = hashlib.sha256((hash_string.encode('utf-8')))

	return hash_value.hexdigest(), data_frame


def AddPostgresSettings(hash_value, settings):

	settings_set = PostgresSettingsSet.objects.filter(settings_sha256=hash_value).get()

	settings_set_id = settings_set.postgres_settings_set_id

	# now parsing all settings
	for index, row in settings.iterrows():
		name = row['name']
		unit = row['source']
		value = row['setting']

		settings_object = {
		'db_settings_id': settings_set_id,
		'setting_name': name,
		'setting_unit': unit,
		'setting_value': value
		}

		serializer = PostgresSettingsSerializer(data=settings_object)

		if serializer.is_valid():
				serializer.save()

		else:
			raise RuntimeError('Invalid Postgres settings.')


def ParsePgBenchOptions(json_file):

	result = {
		'clients': json_file['pgbench']['clients'],
		'init': json_file['results']['init'],
		'warmup': json_file['results']['warmup'],
		'scale': json_file['pgbench']['scale'],
		'duration': json_file['pgbench']['duration'],
	}

	return result


def ParsePgBenchStatementLatencies(statement_latencies): 

	# extract the nonempty statements
	statements = statement_latencies.split("\n")
	statements = list(filter(None, statements))

	for statement in statements:
		line = re.findall('\d+\.\d+', statement)[0]
		line_id = 0
		text = (statement.split(line)[1]).strip()
		print(text)

		# todo
		



def ParsePgBenchResults(json, run_id, benchmark_id):

	for result in json:

		# remove statement latencies
		statement_latencies = result['statement_latencies']

		ParsePgBenchStatementLatencies(statement_latencies)

		result.pop('statement_latencies')

		result['run_id'] = run_id
		result['benchmark_config'] = benchmark_id

		result_serializer = PgBenchResultSerializer(data=result)

		if result_serializer.is_valid():
				result_valid = result_serializer.save()

		else:
			print(result_serializer.errors)
			raise RuntimeError('Invalid PgBench data.')


