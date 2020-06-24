# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import shortuuid
import json
import pandas
import io
import csv
import hashlib

from django.contrib.auth.hashers import make_password
from rest_framework.pagination import PageNumberPagination

from rest_framework import permissions, renderers, viewsets, mixins, authentication, serializers, status

from machines.models import Machine
from postgres.models import PostgresSettingsSet
from postgres.serializers import PostgresSettingsSetSerializer
from runs.models import RunInfo
from systems.serializers import LinuxInfoSerializer
from runs.serializers import RunInfoSerializer, RuntimeSerializer

from runs.parsing_functions import ParseLinuxData, GetHash, AddPostgresSettings

# todo: benchmarks serializers, hashing of postgres settings


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import mixins, status, permissions

class RunViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	queryset =  RunInfo.objects.all().order_by('add_time')
	serializer_class = RunInfoSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )


@api_view(['POST'])
@permission_classes((permissions.AllowAny, ))
def CreateRunInfo(request, format=None):

	data = request.data

	json_data = json.dumps(data[0], ensure_ascii=False)
	json_data = json.loads(json_data)

	from django.db import transaction

	# check if machine exists
	try:
		secret = request.META.get("HTTP_AUTHORIZATION")

		try: 
			ret = Machine.objects.filter(machine_secret=secret).get()
			test_machine = ret.machine_id

		except Machine.DoesNotExist:
			raise RuntimeError("The machine is unavailable.")

		with transaction.atomic():

			os = 'L'
			os_name = json_data['linux']['os']['release']
			os_version = json_data['linux']['os']['version']

			linux_data = ParseLinuxData(json_data)

			linuxInfo = LinuxInfoSerializer(data=linux_data)
			linuxInfoRet = None

			if linuxInfo.is_valid():
				linuxInfoRet = linuxInfo.save()

			else:
				msg = 'LinuxInfo is invalid.'
				raise RuntimeError(msg)

			branch = json_data['postgres']['branch']
			commit = json_data['postgres']['commit']

			postgres_hash, postgres_hash_object = GetHash(json_data['postgres_settings'])

			postgres_configuration = {'settings_sha256': postgres_hash}

			postgres_info = PostgresSettingsSetSerializer(data=postgres_configuration)

			if postgres_info.is_valid():

				try:
					ret = PostgresSettingsSet.objects.filter(settings_sha256=postgres_hash).get()

					pg_settings_id = ret.settings_sha256

				except PostgresSettingsSet.DoesNotExist:

					postgres_info.save()
					AddPostgresSettings(postgres_hash, postgres_hash_object)

			else:
				msg = 'Error hashing Postgres configuration.'
				print(postgres_info.errors)
				raise RuntimeError(msg)

			'''

			if postgres_settings_set.is_valid():
				postgres_settings_set.save()


			runtime_info = json_data['runtime_log']

			times = RuntimeSerializer(data=runtime_info)

			if 'git_clone_log' not in json_data:
				git_clone_log = ''
			else:
				git_clone_log = json_data['git_clone_log']

			if 'build_log' not in json_data:
				build_log = ''
			else:
				build_log = json_data['build_log']

			if 'cleanup_log' not in json_data:
				cleanup_log = ''
			else:
				cleanup_log = json_data['cleanup_log']

			if 'configure_log' not in json_data:
				configure_log = ''
			else:
				configure_log = json_data['configure_log']

			if 'install_log' not in json_data:
				install_log = ''
			else:
				install_log = json_data['install_log']

			postgres_log = json_data['pg_ctl']
			benchmark_log = json_data['pgbench_log']
			
			pgbench = json_data['pgbench']

			pgbench_info = PgBenchBenchmarkSerializer(data=pgbench)
			pgbenchRet = None

			if pgbench_info.is_valid():
				pgbenchRet = pgbench_info.save()

			'''

			# save???
			

	except Exception as e:
		msg = 'Upload error: ' + e.__str__()
		print(msg)
		return Response(msg, status=status.HTTP_406_NOT_ACCEPTABLE)

	print('Upload successful!')
	return Response(status=status.HTTP_201_CREATED)