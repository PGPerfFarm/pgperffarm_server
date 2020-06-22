import pandas
import csv
import json
import hashlib
import io


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

	return hash_value.hexdigest()