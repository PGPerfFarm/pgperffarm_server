# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
import shortuuid

from django.contrib.auth.hashers import make_password
from rest_framework.pagination import PageNumberPagination

from records.exception import TestDataUploadError
from records.filters import TestRecordListFilter
from machines.models import Machine
from records.models import TestCategory, TestBranch
from rest_api.settings import DB_ENUM
from records.serializers import *

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import mixins, status, permissions

from rest_framework import viewsets
from .models import TestRecord
import json


class StandardResultsSetPagination(PageNumberPagination):
	page_size = 20
	page_size_query_param = 'page_size'
	max_page_size = 100


class BigResultsSetPagination(PageNumberPagination):
	page_size = 1000
	page_size_query_param = 'page_size'


class TestBranchListViewSet(viewsets.ModelViewSet):
	"""
	List test branches
	"""

	queryset = TestBranch.objects.all().order_by('branch_order','add_time')
	serializer_class = TestBranchSerializer
	pagination_class = BigResultsSetPagination


class TestCategoryViewSet(viewsets.ModelViewSet):
	"""
	List test categories
	"""

	queryset = TestCategory.objects.all().order_by('cate_name')
	serializer_class = TestCategorySerializer
	pagination_class = StandardResultsSetPagination


class TestRecordListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
	"""
	List test records
	"""

	queryset = TestRecord.objects.all().order_by('add_time')
	serializer_class = TestRecordListSerializer
	pagination_class = StandardResultsSetPagination
	filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
	lookup_field = 'uuid'
	permission_classes = (permissions.AllowAny, )


class TestRecordDetailViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	"""
	Detail test records
	"""
	lookup_field = 'uuid'
	queryset = TestRecord.objects.all().order_by('add_time')
	serializer_class = TestRecordDetailSerializer
	permission_classes = (permissions.AllowAny, )


class MachineHistoryRecordViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	"""
	Machine info page
	"""
	lookup_field = 'sn'
	queryset = Machine.objects.all().order_by('add_time')
	serializer_class = MachineHistoryRecordSerializer
	permission_classes = (permissions.AllowAny, )


class TestRecordListByBranchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
	"""
	List test records (/status)
	"""
	queryset = TestRecord.objects.order_by('test_machine__alias','-add_time').distinct('test_machine__alias').all()
	serializer_class = TestRecordListSerializer
	pagination_class = StandardResultsSetPagination
	filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


@api_view(['POST'])
@permission_classes((permissions.AllowAny, ))
def TestRecordCreate(request, format=None):
	"""
	Receive data from client
	"""
	data = request.data

	json_data = json.dumps(data[0], ensure_ascii=False)
	json_data = json.loads(json_data)
	# obj = data[0].pgbench
	# jsLoads = json.loads(data[0])

	from django.db import transaction

	try:
		secret = request.META.get("HTTP_AUTHORIZATION")
		ret = Machine.objects.filter(machine_secret=secret, state='A').get()
		test_machine = ret.id
		if test_machine <= 0:
			raise TestDataUploadError("The machine is unavailable.")

		record_hash = make_password(str(json_data), 'pg_perf_farm')
		r = TestRecord.objects.filter(hash=record_hash).count()
		if r != 0:
			raise TestDataUploadError('The same record already exists, please do not submit it twice.')

		with transaction.atomic():

			if 'linux' not in json_data:
				print('linuxInfo not found')
				linuxInfo = LinuxInfoSerializer(data={'mounts': 'none', 'cpuinfo': 'none', 'sysctl': 'none', 'meminfo': 'none'})

			else:
				linux_data = json_data['linux']
				linuxInfo = LinuxInfoSerializer(data=linux_data)
				linuxInfoRet = None

			if linuxInfo.is_valid():
				linuxInfoRet = linuxInfo.save()

			else:
				msg = 'linuxInfo invalid'
				raise TestDataUploadError(msg)

			meta_data = json_data['meta']
			metaInfo = MetaInfoSerializer(data=meta_data)
			metaInfoRet = None
			if metaInfo.is_valid():
				metaInfoRet = metaInfo.save()
			else:
				msg = 'metaInfo invalid'
				raise TestDataUploadError(msg)

			pg_data = json_data['postgres']
			branch_str = pg_data['branch']

			if (branch_str == 'master'):
				branch_str = 'HEAD'

			branch = TestBranch.objects.filter(branch_name__iexact=branch_str, is_accept=True).get()

			if not branch:
				raise TestDataUploadError('The branch name is unavailable.')

			commit = pg_data['commit']
			pg_settings = pg_data['settings']

			filtered = ['checkpoint_timeout','work_mem','shared_buffers','maintenance_work_mem','max_wal_size','min_wal_size']

			for item in filtered:
				if item.isdigit():
					pg_settings[item] = int(pg_settings[item])
				# pg_settings[item] = pg_settings[item].encode('utf-8')
				# pg_settings[item] = filter(str.isdigit, pg_settings[item])

			pg_settings['log_checkpoints'] = DB_ENUM['general_switch'][pg_settings['log_checkpoints']]
			pgInfo = CreatePGInfoSerializer(data=pg_settings)
			pgInfoRet = None

			if pgInfo.is_valid():
				pgInfoRet = pgInfo.save()

			else:
				msg = pgInfo.errors
				raise TestDataUploadError(msg)

			test_record_data = {
				'pg_info': pgInfoRet.id,
				'linux_info': linuxInfoRet.id,
				'meta_info': metaInfoRet.id,
				'test_machine': test_machine,
				'test_desc': 'here is desc',
				'meta_time': metaInfoRet.date,
				'hash': record_hash,
				'commit': commit,
				'branch': branch.id,
				'uuid': shortuuid.uuid()
			}

			testRecord = CreateTestRecordSerializer(data=test_record_data)
			testRecordRet = None

			if testRecord.is_valid():
				testRecordRet = testRecord.save()

			else:
				msg = 'testRecord invalid'
				print(testRecord.errors)
				raise TestDataUploadError(msg)

			pgbench = json_data['pgbench']
			# print(type(ro))
			ro = pgbench['ro']

			#for tag, tag_list in pgbench.iteritems():
			for tag, tag_list in pgbench.items():
				#print(tag)
				#print(tag_list)

				test_cate = TestCategory.objects.get(cate_sn=tag)

				if not test_cate:
					continue
				else:
					print(test_cate.cate_name)

				for scale, dataset_list in tag_list.items():

					for client_num, dataset in dataset_list.items():

						test_dataset_data = {
							'test_record': testRecordRet.id,
							'clients': client_num,
							'scale': scale,
							'std': dataset['std'],
							'metric': dataset['metric'],
							'median': dataset['median'],
							'test_cate': test_cate.id,
							# status, percentage will calc by receiver
							'status': -1,
							'percentage': 0.0,
						}

						testDateSet = CreateTestDateSetSerializer(data=test_dataset_data)
						testDateSetRet = None

						if testDateSet.is_valid():
							testDateSetRet = testDateSet.save()
						else:
							print(testDateSet.errors)
							msg = 'testDateSet invalid'
							raise TestDataUploadError(msg)

						test_result_list = dataset['results']

						for test_result in test_result_list:
							test_result_data = test_result
							test_result_data['test_dataset'] = testDateSetRet.id
							test_result_data['mode'] = DB_ENUM['mode'][test_result_data['mode']]
							testResult = CreateTestResultSerializer(data=test_result_data)

							testResultRet = None

							if testResult.is_valid():
								testResultRet = testResult.save()

							else:
								print(testResult.errors)
								msg = testResult.errors
								raise TestDataUploadError(msg)


	except Exception as e:
		msg = 'Upload error: ' + e.__str__()
		print(msg)
		return Response(msg, status=status.HTTP_406_NOT_ACCEPTABLE)

	print('Upload successful!')
	return Response(status=status.HTTP_201_CREATED)
