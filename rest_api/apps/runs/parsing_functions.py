import pandas
import csv
import json
import hashlib
import io
import re

from postgres.models import PostgresSettingsSet
from postgres.serializers import PostgresSettingsSerializer
from benchmarks.serializers import PgBenchResultSerializer, PgBenchStatementSerializer, PgBenchRunStatementSerializer


def ParseSysctl(data):
	
	json = {}

	r = re.search('kernel.shmmax = ([0-9]+)\n', data)
	if r:
		json.update({'shmmax': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('kernel.shmmin = ([0-9]+)\n', data)
	if r:
		json.update({'shmmin': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('kernel.shmall = ([0-9]+)\n', data)
	if r:
		json.update({'shmall': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('kernel.shmseg = ([0-9]+)\n', data)
	if r:
		json.update({'shmseg': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('kernel.shmmni = ([0-9]+)\n', data)
	if r:
		json.update({'shmmni': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('kernel.semmni = ([0-9]+)\n', data)
	if r:
		json.update({'semmni': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('kernel.semmns = ([0-9]+)\n', data)
	if r:
		json.update({'semmns': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('kernel.semmsl = ([0-9]+)\n', data)
	if r:
		json.update({'semmsl': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('kernel.semmap = ([0-9]+)\n', data)
	if r:
		json.update({'semmap': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('kernel.semvmx = ([0-9]+)\n', data)
	if r:
		json.update({'semvmx': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('vm.nr_hugepages = ([0-9]+)\n', data)
	if r:
		json.update({'nr_hugepages': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('vm.nr_hugepages_mempolicy = ([0-9]+)\n', data)
	if r:
		json.update({'nr_hugepages_mempolicy': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('vm.nr_overcommit_hugepages = ([0-9]+)\n', data)
	if r:
		json.update({'nr_overcommit_hugepages': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('vm.overcommit_kbytes = ([0-9]+)\n', data)
	if r:
		json.update({'overcommit_kbytes': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('vm.overcommit_memory = ([0-9]+)\n', data)
	if r:
		json.update({'overcommit_memory': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('vm.overcommit_ratio = ([0-9]+)\n', data)
	if r:
		json.update({'overcommit_ratio': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('vm.swappiness = ([0-9]+)\n', data)
	if r:
		json.update({'swappiness': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('vm.numa_stat = ([0-9]+)\n', data)
	if r:
		json.update({'numa_stat': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('vm.numa_zonelist_order = ([0-9]+)\n', data)
	if r:
		json.update({'numa_zonelist_order': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('vm.dirty_background_bytes = ([0-9]+)\n', data)
	if r:
		json.update({'dirty_background_bytes': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('vm.dirty_background_ratio = ([0-9]+)\n', data)
	if r:
		json.update({'dirty_background_ratio': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('vm.dirty_bytes = ([0-9]+)\n', data)
	if r:
		json.update({'dirty_bytes': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('vm.dirty_expire_centisecs = ([0-9]+)\n', data)
	if r:
		json.update({'dirty_expire_centisecs': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('vm.dirty_ratio = ([0-9]+)\n', data)
	if r:
		json.update({'dirty_ratio': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('vm.dirty_writeback_centisecs = ([0-9]+)\n', data)
	if r:
		json.update({'dirty_writeback_centisecs': r.group(1)})
		data.replace(r.group(0), '')

	r = re.search('vm.dirtytime_expire_seconds = ([0-9]+)\n', data)
	if r:
		json.update({'dirtytime_expire_seconds': r.group(1)})
		data.replace(r.group(0), '')

	return data, json


def ParseLinuxData(json_data):

	if ('brand' in json_data['linux']['cpu']['information']):
		brand = json_data['linux']['cpu']['information']['brand']

	else:
		brand = json_data['linux']['cpu']['information']['brand_raw']

	if ('hz_actual_raw' in json_data['linux']['cpu']['information']):
		hz = json_data['linux']['cpu']['information']['hz_actual_raw'][0]

	else:
		hz = json_data['linux']['cpu']['information']['hz_actual'][0]

	sysctl_log, sysctl_known = ParseSysctl(json_data['sysctl_log'])

	result = {
		'cpu_brand': brand,
		'hz': hz,
		'cpu_cores': json_data['linux']['cpu']['information']['count'],
		'total_memory': json_data['linux']['memory']['virtual']['total'],
		'total_swap': json_data['linux']['memory']['swap']['total'],
		'mounts': json_data['linux']['memory']['mounts'],
		'sysctl': sysctl_log
	}

	return result, sysctl_known


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
					raise RuntimeError('Invalid PgBench run statement data.')

		else:
			raise RuntimeError('Invalid PgBench statement data.')



def ParsePgBenchResults(item, run_id, benchmark_id):

	json = item['iterations']

	for result in json:

		# remove statement latencies
		statement_latencies = result['statement_latencies']

		result.pop('statement_latencies')
		result.pop('clients')
		result.pop('threads')

		result['run_id'] = run_id
		result['benchmark_config'] = benchmark_id

		result_serializer = PgBenchResultSerializer(data=result)

		if result_serializer.is_valid():
				result_valid = result_serializer.save()

				ParsePgBenchStatementLatencies(statement_latencies, result_valid.pgbench_result_id)

		else:
			raise RuntimeError('Invalid PgBench data.')


