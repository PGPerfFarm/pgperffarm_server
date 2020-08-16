import csv
import json
import hashlib
import io
import re
import copy
from datetime import datetime

from postgres.models import PostgresSettingsSet
from postgres.serializers import PostgresSettingsSerializer
from benchmarks.models import PgBenchBenchmark, PgBenchResult
from benchmarks.serializers import PgBenchResultSerializer, PgBenchStatementSerializer, PgBenchRunSingleStatementSerializer, PgBenchLogSerializer
from systems.models import Kernel


def ParseSysctl(raw_data):

	data = json.loads(raw_data)
	json_dict = {}

	known_sysctl_linux = Kernel.objects.filter(kernel_id=1).get()

	for parameter in known_sysctl_linux.sysctl:

		if parameter in data:
			json_dict.update({parameter: data[parameter]})

	known_sysctl_mac = Kernel.objects.filter(kernel_id=2).get()

	for parameter in known_sysctl_mac.sysctl:

		if parameter in data:
			json_dict.update({parameter: data[parameter]})

	if json_dict == {}:
		return 'known sysctl info not found'

	else:
		return json_dict


def Hash(json_data):

	hash_value = hashlib.sha256(json.dumps(json_data).encode('utf-8'))
	return hash_value.hexdigest()


def ParseLinuxData(json_data):

	if ('brand' in json_data['system']['cpu']['information']):
		brand = json_data['system']['cpu']['information']['brand']

	else:
		brand = json_data['system']['cpu']['information']['brand_raw']

	if ('hz_actual_raw' in json_data['system']['cpu']['information']):
		hz = json_data['system']['cpu']['information']['hz_actual_raw'][0]

	else:
		hz = json_data['system']['cpu']['information']['hz_actual'][0]

	sysctl = ParseSysctl(json_data['sysctl_log'])

	result = {
		'cpu_brand': brand,
		'hz': hz,
		'cpu_cores': json_data['system']['cpu']['information']['count'],
		'total_memory': json_data['system']['memory']['virtual']['total'],
		'total_swap': json_data['system']['memory']['swap']['total'],
		'mounts_hash': Hash(json_data['system']['memory']['mounts']),
		'mounts': json_data['system']['memory']['mounts'],
		'sysctl': sysctl,
		'sysctl_hash': Hash(sysctl)
	}

	return result


def GetHash(postgres_settings):

	reader = csv.DictReader(io.StringIO(postgres_settings))
	postgres_settings_json = json.loads(json.dumps(list(reader)))

	hash_json = []

	for setting in postgres_settings_json:
		if setting['source'] != "default" and setting['source'] != "client":
			hash_json.append(setting)

	hash_string = Hash(hash_json)

	return hash_string, hash_json


def AddPostgresSettings(hash_value, settings):

	settings_set = PostgresSettingsSet.objects.filter(settings_sha256=hash_value).get()

	settings_set_id = settings_set.postgres_settings_set_id

	# now parsing all settings
	for row in settings:
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
			error = serializer.errors
			raise RuntimeError(error)


def ParsePgBenchOptions(item, clients):

	result = {
		'clients': clients,
		'scale': item['scale'],
		'duration': item['duration'],
		'read_only': item['read_only']
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

		try:
			statement_valid = PgBenchStatement.objects.filter(statement=text).get()

		except PgBenchStatement.DoesNotExist:

			pgbench_statement = {'statement': text}
			statement_serializer = PgBenchStatementSerializer(data=pgbench_statement)

			if statement_serializer.is_valid():
				statement_valid = statement_serializer.save()

			else:
				error = statement_serializer.errors
				raise RuntimeError(error)

		data = {
				'latency': latency,
				'line_id': line_id,
				'pgbench_result_id': pgbench_result_id,
				'result_id': statement_valid.pgbench_statement_id
				}

		run_statement_serializer = PgBenchRunSingleStatementSerializer(data=data)

		if run_statement_serializer.is_valid():
			run_statement_serializer.save()
			line_id += 1

		else:
			error = run_statement_serializer.errors
			raise RuntimeError(error)


def ParsePgBenchLogValues(result, values):

	lines = values.splitlines()
	for line in lines:
		results = line.split()

		date = datetime.utcfromtimestamp(int(results[0])).strftime("%Y-%m-%dT%H:%M:%S%z")

		log = {
			'pgbench_result_id': result.pgbench_result_id,
			'interval_start': date,
			'num_transactions': results[1],
			'sum_latency': results[2],
			'sum_latency_2': results[3],
			'min_latency': results[4],
			'max_latency': results[5],
		}

		log_serializer = PgBenchLogSerializer(data=log)

		if log_serializer.is_valid():
			log_serializer.save()

		else:
			error = log_serializer.errors
			raise RuntimeError(error)


def ParsePgBenchLogs(result, log_array, iteration):

	found = False

	for log in log_array:

		for key, value in log.items():

			# tag-scale-duration-clients-iteration
			configs = key.split('-')

			if configs[1] == 'ro':
				read_only = True
			else:
				read_only = False

			# first of all, check that the config of each benchmark actually exists
			pgbench_config = PgBenchBenchmark.objects.filter(clients=configs[4], scale=configs[2], duration=configs[3], read_only=read_only).get()

			# then, check if it is the same as the test result
			if pgbench_config.pgbench_benchmark_id == result.benchmark_config.pgbench_benchmark_id:
				if int(configs[5]) == iteration:
					ParsePgBenchLogValues(result, value)
					found = True

	# if no match has been found, return error
	if not found:
		raise RuntimeError('Invalid PgBench logs.')


def ParsePgBenchResults(item, run_id, pgbench_log):

	json = item['iterations']
	iterations = 0

	for client in item['clients']:

		for result in json:

			if int(result['clients']) == client:

				data = copy.deepcopy(result)

				pgbench_config = PgBenchBenchmark.objects.filter(clients=data['clients'], scale=item['scale'], duration=item['duration'], read_only=item['read_only']).get()

				pgbench_result_last = PgBenchResult.objects.order_by('-pgbench_result_id').first()

				if pgbench_result_last is None:
					iterations = 0

				# assuming results get added in order
				elif (pgbench_result_last.benchmark_config.pgbench_benchmark_id == pgbench_config.pgbench_benchmark_id):
					iterations += 1

				else:
					iterations = 0

				# remove statement latencies
				statement_latencies = data['statement_latencies']

				data.pop('statement_latencies')
				data.pop('clients')
				data.pop('threads')

				data['run_id'] = run_id
				data['benchmark_config'] = pgbench_config.pgbench_benchmark_id

				result_serializer = PgBenchResultSerializer(data=data)

				if result_serializer.is_valid():
						result_valid = result_serializer.save()

						ParsePgBenchLogs(result_valid, pgbench_log, iterations)
						ParsePgBenchStatementLatencies(statement_latencies, result_valid.pgbench_result_id)

				else:
					error = result_serializer.errors
					raise RuntimeError(error)








