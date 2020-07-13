import pandas
import csv
import json
import hashlib
import io
import re

from postgres.models import PostgresSettingsSet
from postgres.serializers import PostgresSettingsSerializer
from benchmarks.serializers import PgBenchResultSerializer, PgBenchStatementSerializer, PgBenchRunStatementSerializer

def ParseLinuxData(json_data):

	if ('brand' in json_data['linux']['cpu']['information']):
		brand = json_data['linux']['cpu']['information']['brand']

	else:
		brand = json_data['linux']['cpu']['information']['brand_raw']

	result = {
		'cpu_brand': brand,
		'hz': ','.join(str(json_data['linux']['cpu']['information']['hz_actual'])),
		'cpu_cores': json_data['linux']['cpu']['information']['count'],
		'total_memory': json_data['linux']['memory']['virtual']['total'],
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


def ParsePgBenchOptions(json_file, clients):

	result = {
		'clients': clients,
		'init': json_file['results']['init'],
		'warmup': json_file['results']['warmup'],
		'scale': json_file['pgbench']['scale'],
		'duration': json_file['pgbench']['duration'],
	}

	return result


def ParsePgBenchStatementLatencies(statement_latencies, pgbench_result_id): 

	# extract the nonempty statements
	statements = statement_latencies.split("\n")
	statements = list(filter(None, statements))

	line_id = 0

	for statement in statements:
		latency = re.findall('\d+\.\d+', statement)[0]
		text = (statement.split(latency)[1]).strip()
		
		pgbench_statement = {'statement': text}

		statement_serializer = PgBenchStatementSerializer(data=pgbench_statement)

		if statement_serializer.is_valid():
				statement_valid = statement_serializer.save()

				data = {
					'latency': latency,
					'line_id': line_id,
					'pgbench_result_id': pgbench_result_id,
					'result_id': statement_valid.pgbench_statement_id
					}

				run_statement_serializer = PgBenchRunStatementSerializer(data=data)

				if run_statement_serializer.is_valid():
					run_statement_serializer.save()
					line_id += 1

				else:
					print(run_statement_serializer.errors)
					raise RuntimeError('Invalid PgBench run statement data.')

		else:
			raise RuntimeError('Invalid PgBench statement data.')



def ParsePgBenchResults(json, run_id, benchmark_id):

	for result in json:

		# remove statement latencies
		statement_latencies = result['statement_latencies']

		result.pop('statement_latencies')
		result.pop('clients')

		result['run_id'] = run_id
		result['benchmark_config'] = benchmark_id

		result_serializer = PgBenchResultSerializer(data=result)

		if result_serializer.is_valid():
				result_valid = result_serializer.save()

				ParsePgBenchStatementLatencies(statement_latencies, result_valid.pgbench_result_id)


		else:
			raise RuntimeError('Invalid PgBench data.')


