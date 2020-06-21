# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import shortuuid
import json

from django.contrib.auth.hashers import make_password
from rest_framework.pagination import PageNumberPagination

from rest_framework import permissions, renderers, viewsets, mixins, authentication, serializers, status

from machines.models import Machine
from postgres.models import PostgresSettingsSet
from runs.models import RunInfo
from systems.serializers import LinuxInfoSerializer
from runs.serializers import RunInfoSerializer, RuntimeSerializer

# todo: benchmarks serializers, hashing of postgres settings


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import mixins, status, permissions

class RunViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
	"""
	List all machines
	"""
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
		ret = Machine.objects.filter(machine_secret=secret).get()
		test_machine = ret.machine_id
		if test_machine <= 0:
			raise RuntimeError("The machine is unavailable.")

		with transaction.atomic():

			os = 'L'
			os_name = json_data['linux']['os']['release']
			os_version = json_data['linux']['os']['version']

			linux_data = {
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

			linuxInfo = LinuxInfoSerializer(data=linux_data)
			linuxInfoRet = None

			if linuxInfo.is_valid():
				linuxInfoRet = linuxInfo.save()

			else:
				msg = 'linuxInfo invalid'
				raise RuntimeError(msg)

			branch = json_data['postgres']['branch']
			commit = json_data['postgres']['commit']

			postgres_settings = json_data['postgres_settings']

			'''
			postgres_info = PostgresSettingsSetSerializer(data=postgres_settings)

			# hash set is returned
			ret = PostgresSettingsSet.objects.filter(settings_sha256=postgres_info).get()

			if ret.settings_sha256 == postgres_info:
				# existing configuration
				postgres_settings_set = PostgresSettingsSerializer()

			else:
				if postgres_info.is_valid():
					postgres_info.save()

			if postgres_settings_set.is_valid():
				postgres_settings_set.save()

			'''

			

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

			'''
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