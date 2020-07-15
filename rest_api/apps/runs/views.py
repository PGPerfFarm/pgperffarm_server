# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import shortuuid
import json
import pandas
import io
import csv
import hashlib


from rest_framework import permissions, renderers, viewsets, mixins, authentication, serializers, status
from django.db import IntegrityError
from django.db.models import Count

from machines.models import Machine
from postgres.models import PostgresSettingsSet
from postgres.serializers import PostgresSettingsSetSerializer
from runs.models import RunInfo, GitRepo
from runs.serializers import RunInfoSerializer, GitRepoSerializer, BranchSerializer, LastRunsSerializer
from systems.serializers import LinuxInfoSerializer, CompilerSerializer
from systems.models import LinuxInfo, Compiler
from benchmarks.models import PgBenchBenchmark
from benchmarks.serializers import PgBenchBenchmarkSerializer
from machines.serializers import MachineRunsSerializer

from runs.parsing_functions import ParseLinuxData, GetHash, AddPostgresSettings, ParsePgBenchOptions, ParsePgBenchResults

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import mixins, status, permissions


class RunViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	queryset = RunInfo.objects.all()
	serializer_class = RunInfoSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )


class LastRunsViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	queryset = Machine.objects.all()

	serializer_class = MachineRunsSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )

	def get_queryset(self):
		return Machine.objects.filter(machine_id=self.kwargs['pk'])


class BranchViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	queryset = RunInfo.objects.all()
	serializer_class = BranchSerializer

	def get_queryset(self):
		return RunInfo.objects.values('git_branch').annotate(results=Count('run_id'), machines=Count('machine_id', distinct=True))



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
			machine = Machine.objects.filter(machine_secret=secret).get()
			machine_id = machine.machine_id

		except Machine.DoesNotExist:
			raise RuntimeError("The machine is unavailable.")

		with transaction.atomic():

			try: 
				compiler_result = Compiler.objects.filter(compiler=json_data['compiler']).get()
				compiler_id = compiler_result.compiler_id

			except Compiler.DoesNotExist:

				compiler = {'compiler': json_data['compiler']}

				compiler_serializer = CompilerSerializer(data=compiler)

				if compiler_serializer.is_valid():
					compiler_valid = compiler_serializer.save()
					compiler_id = compiler_valid.compiler_id

				else:
					msg = 'Compiler information is invalid.'
					raise RuntimeError(msg)

			try: 
				repo_result = GitRepo.objects.filter(url=json_data['git']['remote']).get()
				repo_id = repo_result.git_repo_id

			except GitRepo.DoesNotExist:

				repo = {'url': json_data['git']['remote']}

				repo_serializer = GitRepoSerializer(data=repo)

				if repo_serializer.is_valid():
					repo_valid = repo_serializer.save()
					repo_id = repo_valid.git_repo_id

				else:
					msg = 'Git information is invalid.'
					raise RuntimeError(msg)


			os = 'L'
			os_name = json_data['linux']['os']['release']
			os_version = json_data['linux']['os']['version']

			linux_data = ParseLinuxData(json_data)

			try: 
				linux_valid_info = LinuxInfo.objects.filter(cpu_brand=linux_data['cpu_brand'], cpu_cores=linux_data['cpu_cores'], hz=linux_data['hz'], total_memory=linux_data['total_memory']).get()
			

			except LinuxInfo.DoesNotExist:

				linux_info = LinuxInfoSerializer(data=linux_data)

				if linux_info.is_valid():
					linux_valid_info = linux_info.save()

				else:
					msg = 'Linux information is invalid.'
					print(linux_info.errors)
					raise RuntimeError(msg)

			branch = json_data['git']['branch']
			commit = json_data['git']['commit']

			postgres_hash, postgres_hash_object = GetHash(json_data['postgres_settings'])

			postgres_configuration = {'settings_sha256': postgres_hash}

			postgres_info = PostgresSettingsSetSerializer(data=postgres_configuration)

			if postgres_info.is_valid():

				try:
					obj = PostgresSettingsSet.objects.filter(settings_sha256=postgres_hash).get()

					pg_settings_id = obj.postgres_settings_set_id

				except PostgresSettingsSet.DoesNotExist:

					postgres_valid_info = postgres_info.save()
					AddPostgresSettings(postgres_hash, postgres_hash_object)

					pg_settings_id = postgres_valid_info.postgres_settings_set_id

			else:
				msg = 'Error hashing Postgres configuration.'
				raise RuntimeError(msg)

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

			# also create the benchmark
			for client in json_data['pgbench']['clients']:
				pgbench = ParsePgBenchOptions(json_data, client)

				pgbench_info = PgBenchBenchmarkSerializer(data=pgbench)

				if pgbench_info.is_valid():

					try:
						pgbench_valid = PgBenchBenchmark.objects.filter(clients=pgbench['clients'], init=pgbench['init'], scale=pgbench['scale'], duration=pgbench['duration'], read_only=pgbench['read_only']).get()

					except PgBenchBenchmark.DoesNotExist:

						pgbench_valid = pgbench_info.save()

				else:
					msg = 'Error parsing PgBench configuration.'
					raise RuntimeError(msg)

			# before doing anything else related to benchmarks, save the run

			run_info = {
				'machine_id': machine_id,
				'os_type': os,
				'os_name': os_name,
				'os_version': os_version,
				'os_config_info': linux_valid_info.linux_info_id,
				'compiler': compiler_id,
				'git_branch': branch,
				'git_commit': commit,
				'git_clone_log': git_clone_log,
				'configure_log': configure_log,
				'build_log': build_log,
				'install_log': install_log,
				'benchmark_log': benchmark_log,
				'cleanup_log': cleanup_log,
				'postgres_log': postgres_log,
				'postgres_info': pg_settings_id,
				'run_received_time': json_data['run_received_time'],
				'run_start_time': json_data['run_start_time'],
				'run_end_time': json_data['run_end_time'],
				'git_pull_runtime': json_data['git_pull_runtime'],
				'git_clone_runtime': json_data['git_clone_runtime'],
				'git_repo': repo_id,
				'configure_runtime': json_data['configure_runtime'],
				'build_runtime': json_data['build_runtime'],
				'install_runtime': json_data['install_runtime'],
				'benchmark': pgbench_valid.pgbench_benchmark_id,
				'cleanup_runtime': json_data['cleanup_runtime']
			}

			run_info_serializer = RunInfoSerializer(data=run_info)

			if run_info_serializer.is_valid():
				run_valid = run_info_serializer.save()

			else:
				msg = 'Error parsing run configuration.'
				print (run_info_serializer.errors)
				raise RuntimeError(msg)

			# now continue with benchmarks
			ParsePgBenchResults(json_data, run_valid.run_id, pgbench_valid.pgbench_benchmark_id)
			

	except Exception as e:
		msg = 'Upload error: ' + e.__str__()
		print(msg)
		return Response(msg, status=status.HTTP_406_NOT_ACCEPTABLE)

	print('Upload successful!')
	return Response(status=status.HTTP_201_CREATED)