# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
import shortuuid

from django.contrib.auth.hashers import make_password
from django.db.models import Count
# from requests import request
from rest_framework.pagination import PageNumberPagination

from exception import TestDataUploadError
from test_records.filters import TestRecordListFilter
from models import UserMachine, TestCategory, TestBranch
from pgperffarm.settings import DB_ENUM
from user_operation.views import UserMachinePermission
from .serializer import MachineHistoryRecordSerializer, TestStatusRecordListSerializer, TestBranchSerializer
from .serializer import TestRecordListSerializer, TestRecordDetailSerializer, LinuxInfoSerializer, MetaInfoSerializer, \
    PGInfoSerializer, CreateTestRecordSerializer, CreateTestDateSetSerializer, TestResultSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import status

from rest_framework import viewsets
from .models import TestRecord
import json


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100

class BigResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'

class TestBranchListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    List test records
    """

    queryset = TestBranch.objects.all().order_by('branch_order')
    serializer_class = TestBranchSerializer
    pagination_class = BigResultsSetPagination

class TestRecordListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    List test records
    """

    queryset = TestRecord.objects.all().order_by('add_time')
    serializer_class = TestRecordListSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = TestRecordListFilter

class TestRecordListByBranchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    List test records
    """

    queryset = TestRecord.objects.order_by('test_machine_id','-add_time').distinct('test_machine_id').all()
    serializer_class = TestRecordListSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = TestRecordListFilter

# @api_view(['GET'])
# def GetStatusRecordList(request, format=None):
#     """
#     List lastest test records involve all branches
#     """
#
#     queryset = TestBranch.objects.all().order_by('branch_order').values_list('id','branch_name').annotate(num_records=Count('testrecord')).filter(num_records__gt=0)
#     # print queryset # <QuerySet [(1, u'HEAD', 3), (2, u'10_STABLE', 2)]>
#
#     ret = {'branch_num':queryset.__len__(),'result':[]}
#     for branch_item in queryset:
#
#         target_record = TestRecord.objects.filter(branch_id=branch_item[0]).order_by('test_machine_id','-add_time').distinct('test_machine_id').all()
#         # print target_record  # <QuerySet [(1, u'HEAD', 3), (2, u'10_STABLE', 2)]>
#         data = TestRecordListSerializer(target_record,many=True)
#         obj = {'branch':branch_item[1],'data':data.data}
#         ret["result"].append(obj)
#     # msg = 'ok!'
#     return Response(ret, status=status.HTTP_201_CREATED)


class TestRecordDetailViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    detail test records
    """
    lookup_field = 'uuid'
    queryset = TestRecord.objects.all().order_by('add_time')
    serializer_class = TestRecordDetailSerializer
    # pagination_class = StandardResultsSetPagination

class MachineHistoryRecordViewSet( mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    detail test records
    """
    lookup_field = 'machine_sn'
    queryset = UserMachine.objects.all().order_by('add_time')
    serializer_class = MachineHistoryRecordSerializer
    # pagination_class = StandardResultsSetPagination

@api_view(['POST'])
@permission_classes((UserMachinePermission, ))
def TestRecordCreate(request, format=None):
    """
    Receive data from client
    """

    data = request.data

    print type(data[0])
    json_data = json.dumps(data[0], encoding="UTF-8", ensure_ascii=False)
    json_data = json.loads(json_data, encoding="UTF-8")
    # obj = data[0].pgbench
    # jsLoads = json.loads(data[0])

    # todo get machine by token
    test_machine = 1

    from django.db import transaction

    try:

        record_hash = make_password(str(json_data), 'pg_perf_farm')
        # print(record_hash.__len__()) 77
        r = TestRecord.objects.filter(hash=record_hash).count()
        if r != 0:
            raise TestDataUploadError("The same record already exists, please do not submit it twice.")

        with transaction.atomic():

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
            commit = pg_data['commit']
            pg_settings = pg_data['settings']
            pg_data = {
                'pg_branch': 1
            }
            pgInfo = PGInfoSerializer(data=pg_data)
            pgInfoRet = None
            if pgInfo.is_valid():
                pgInfoRet = pgInfo.save()
            else:
                msg = 'pgInfo invalid'
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
            for tag, tag_list in pgbench.iteritems():
                test_cate = TestCategory.objects.get(cate_sn=tag)
                if not test_cate:
                    continue
                else:
                    print test_cate.cate_name
                for scale, dataset_list in tag_list.iteritems():
                    print "ro[%s]=" % scale, dataset_list
                    for client_num, dataset in dataset_list.iteritems():
                        print 'std is:' + str(dataset['std'])

                        test_dataset_data = {
                            'test_record': testRecordRet.id,
                            'clients': client_num,
                            'scale': scale,
                            'std': dataset['std'],
                            'metric': dataset['metric'],
                            'median': dataset['median'],
                            'test_cate': test_cate.id,
                            # status,percentage will calc by receiver
                            'status': -1,
                            'percentage': 0.0,
                        }
                        testDateSet = CreateTestDateSetSerializer(data=test_dataset_data)
                        testDateSetRet = None
                        if testDateSet.is_valid():
                            print 'dataset valid'
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
                            testResult = TestResultSerializer(data=test_result_data)

                            testResultRet = None
                            if testResult.is_valid():
                                print 'testResult valid'
                                testResultRet = testResult.save()
                            else:
                                print(testResult.errors)
                                msg = 'testResult invalid'
                                raise TestDataUploadError(msg)

    except Exception as e:
        msg = 'upload error:' + str(e).encode('utf-8')
        # todo add log
        return Response(msg, status=status.HTTP_202_ACCEPTED)

    msg = 'upload success!'
    return Response(msg, status=status.HTTP_201_CREATED)
