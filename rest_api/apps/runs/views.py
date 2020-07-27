# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import shortuuid
import json
import pandas
import io
import csv
import hashlib
import re


from rest_framework import permissions, renderers, viewsets, mixins, authentication, serializers, status
from django.db import IntegrityError
from django.db.models import Count

from machines.models import Machine
from machines.serializers import MachineSerializer
from postgres.models import PostgresSettingsSet
from postgres.serializers import PostgresSettingsSetSerializer
from runs.models import RunInfo, GitRepo, Branch
from runs.serializers import RunInfoSerializer, GitRepoSerializer, BranchSerializer, LastRunsSerializer, BranchSerializer
from systems.serializers import HardwareInfoSerializer, CompilerSerializer, KnownSysctlInfoSerializer, KernelSerializer, OsDistributorSerializer, OsVersionSerializer, OsKernelVersionSerializer
from systems.models import HardwareInfo, Compiler, KnownSysctlInfo, Kernel, OsDistributor, OsKernelVersion, OsVersion
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

			os_old = machine.machine_type
			os_new = json_data['kernel']['uname_m']

			if os_old == '':
				machine_serializer = MachineSerializer(machine, data={'machine_type': os_new}, partial=True)

				if machine_serializer.is_valid():
					machine_serializer.save()

				else:
					msg = 'Machine OS information is invalid.'
					raise RuntimeError(msg)

			elif os_old != os_new:
				raise RuntimeError("Machine OS cannot change.")

		except Machine.DoesNotExist:
			raise RuntimeError("The machine is unavailable.")

		with transaction.atomic():

			try:
				os_distributor = OsDistributor.objects.filter(dist_name=json_data['os_information']['distributor']).get()

			except OsDistributor.DoesNotExist:
				distributor = {'dist_name': json_data['os_information']['distributor']}

				distributor_serializer = OsDistributorSerializer(data=distributor)

				if distributor_serializer.is_valid():
					os_distributor = distributor_serializer.save()

				else:
					msg = 'Distributor information is invalid.'
					raise RuntimeError(msg)
			try:
				os_kernel = Kernel.objects.filter(kernel_name=json_data['kernel']['uname_s']).get()

			except Kernel.DoesNotExist:
				kernel = {'kernel_name': json_data['kernel']['uname_s']}

				kernel_serializer = KernelSerializer(data=kernel)

				if kernel_serializer.is_valid():
					os_kernel = kernel_serializer.save()

				else:
					msg = 'Kernel information is invalid.'
					raise RuntimeError(msg)

			try:
				os_version = OsVersion.objects.filter(dist_id=os_distributor.os_distributor_id, release=json_data['os_information']['release'], codename=json_data['os_information']['codename'], description=json_data['os_information']['description']).get()

			except OsVersion.DoesNotExist:
				os = {
					'dist_id': os_distributor.os_distributor_id, 
					'release': json_data['os_information']['release'], 
					'codename': json_data['os_information']['codename'], 
					'description': json_data['os_information']['description']}

				os_serializer = OsVersionSerializer(data=os)

				if os_serializer.is_valid():
					os_version = os_serializer.save()

				else:
					msg = 'Os version information is invalid.'
					raise RuntimeError(msg)

			try:
				os_kernel_version = OsKernelVersion.objects.filter(kernel_id=os_kernel.kernel_id, kernel_release=json_data['kernel']['uname_r'], kernel_version=json_data['kernel']['uname_v']).get()

			except OsKernelVersion.DoesNotExist:
				kernel_version = {
					'kernel_id': os_kernel.kernel_id, 
					'kernel_release': json_data['kernel']['uname_r'], 
					'kernel_version': json_data['kernel']['uname_v']
					}

				os_kernel_version_serializer = OsKernelVersionSerializer(data=kernel_version)

				if os_kernel_version_serializer.is_valid():
					os_kernel_version = os_kernel_version_serializer.save()

				else:
					msg = 'OS kernel version information is invalid.'
					raise RuntimeError(msg)

			compiler_raw = json_data['compiler']
			compiler_match = re.search('compiled by (.*),', compiler_raw)
			if compiler_match:
				compiler = compiler_match.group(1)
			else:
				compiler = 'impossible to parse compiler'

			try: 
				compiler_result = Compiler.objects.filter(compiler=compiler).get()
				compiler_id = compiler_result.compiler_id

			except Compiler.DoesNotExist:

				compiler_serializer = CompilerSerializer(data={'compiler': compiler})

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

			try: 
				branch_result = Branch.objects.filter(name=json_data['git']['branch'], git_repo=repo_id).get()

			except Branch.DoesNotExist:

				branch = {
					'name': json_data['git']['branch'],
					'git_repo': repo_id
				}

				branch_serializer = BranchSerializer(data=branch)

				if branch_serializer.is_valid():
					branch_result = branch_serializer.save()
				
				else:
					msg = 'Branch information is invalid.'
					raise RuntimeError(msg)

			hardware_info_new = ParseLinuxData(json_data)
			try:
				hardware_info_valid = HardwareInfo.objects.filter(cpu_brand=hardware_info_new['cpu_brand'], cpu_cores=hardware_info_new['cpu_cores'], hz=hardware_info_new['hz'], total_memory=hardware_info_new['total_memory'], total_swap=hardware_info_new['total_swap'], sysctl_hash=hardware_info_new['sysctl_hash'], mounts_hash=hardware_info_new['mounts_hash']).get()

			except HardwareInfo.DoesNotExist:

				hardware_info = HardwareInfoSerializer(data=hardware_info_new)

				if hardware_info.is_valid():
					hardware_info_valid = hardware_info.save()

				else:
					msg = 'Hardware information is invalid.'
					raise RuntimeError(msg)

			commit = json_data['git']['commit']

			postgres_hash, postgres_hash_object = GetHash(json_data['postgres_settings'])

			postgres_configuration = {'settings_sha256': postgres_hash}

			try:
				obj = PostgresSettingsSet.objects.filter(settings_sha256=postgres_hash).get()
				pg_settings_id = obj.postgres_settings_set_id

			except PostgresSettingsSet.DoesNotExist:

					postgres_info = PostgresSettingsSetSerializer(data=postgres_configuration)

					if postgres_info.is_valid():

						postgres_valid_info = postgres_info.save()
						pg_settings_id = postgres_valid_info.postgres_settings_set_id
						AddPostgresSettings(postgres_hash, postgres_hash_object)

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

			# before doing anything else related to benchmarks, save the run
			run_info = {
				'machine_id': machine_id,
				'hardware_info': hardware_info_valid.hardware_info_id,
				'compiler': compiler_id,
				'git_branch': branch_result.branch_id,
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
				'cleanup_runtime': json_data['cleanup_runtime'],
				'os_version_id': os_version.os_version_id,
				'os_kernel_version_id': os_kernel_version.os_kernel_version_id,
				'sysctl_raw': json_data['sysctl_log']
			}

			run_info_serializer = RunInfoSerializer(data=run_info)

			if run_info_serializer.is_valid():
				run_valid = run_info_serializer.save()

			else:
				msg = 'Error parsing run configuration.'
				raise RuntimeError(msg)


			# now continue with benchmarks
			for item in json_data['pgbench']:

				for client in item['clients']:
					pgbench = ParsePgBenchOptions(item, client)

					try:
						pgbench_valid = PgBenchBenchmark.objects.filter(clients=client, scale=pgbench['scale'], duration=pgbench['duration'], read_only=pgbench['read_only']).get()

					except PgBenchBenchmark.DoesNotExist:

							pgbench_info = PgBenchBenchmarkSerializer(data=pgbench)

							if pgbench_info.is_valid():
								pgbench_valid = pgbench_info.save()

							else:
								msg = 'Error parsing PgBench configuration.'
								raise RuntimeError(msg)

				ParsePgBenchResults(item, run_valid.run_id, json_data['pgbench_log_aggregate'])

			

	except Exception as e:
		msg = 'Upload error: ' + e.__str__()
		print(msg)
		return Response(msg, status=status.HTTP_406_NOT_ACCEPTABLE)

	print('Upload successful!')
	return Response(status=status.HTTP_201_CREATED)
