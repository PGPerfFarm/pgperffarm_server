import pandas
import csv
import json
import hashlib
import io

from postgres.models import PostgresSettingsSet
from postgres.serializers import PostgresSettingsSerializer

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
			print(serializer.errors)
			raise RuntimeError('Invalid Postgres settings.')


