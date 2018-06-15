# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination

from models import UserMachine, TestCategory
from .serializer import TestRecordSerializer, TestRecordDetailSerializer, LinuxInfoSerializer, MetaInfoSerializer, \
    PGInfoSerializer, CreateTestRecordSerializer, CreateTestDateSetSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from .models import TestRecord, LinuxInfo, MetaInfo, PGInfo, TestBranch
import json


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class TestRecordListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    List test records
    """
    queryset = TestRecord.objects.all()
    serializer_class = TestRecordSerializer
    pagination_class = StandardResultsSetPagination


class TestRecordDetailViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    List test records
    """
    queryset = TestRecord.objects.all()
    serializer_class = TestRecordDetailSerializer
    pagination_class = StandardResultsSetPagination


@api_view(['POST'])
def TestRecordCreate(request, format=None):
    """
    Receive data from client
    """

    # serializers = BizcircleSerializer(data=request.data)
    # if serializers.is_valid():
    #     serializers.save()
    #     return Response(serializers.data, status=status.HTTP_201_CREATED)
    data = request.data

    print type(data[0])
    json_data = json.dumps(data[0], encoding="UTF-8", ensure_ascii=False)
    json_data = json.loads(json_data, encoding="UTF-8")
    # obj = data[0].pgbench
    # jsLoads = json.loads(data[0])

    linux_data = json_data['linux']
    linuxInfo = LinuxInfoSerializer(data=linux_data)
    linuxInfoRet = None
    if linuxInfo.is_valid():
        linuxInfoRet = linuxInfo.save()
    else:
        msg = 'linuxInfo save error'
        return Response(msg, status=status.HTTP_202_ACCEPTED)

    meta_data = json_data['meta']
    metaInfo = MetaInfoSerializer(data=meta_data)
    metaInfoRet = None
    if metaInfo.is_valid():
        metaInfoRet = metaInfo.save()
    else:
        msg = 'metaInfo save error'
        return Response(msg, status=status.HTTP_202_ACCEPTED)

    # pg_data = json_data['postgres']
    pg_data = {
        'pg_branch':1
    }
    pgInfo = PGInfoSerializer(data=pg_data)
    pgInfoRet = None
    if pgInfo.is_valid():
        pgInfoRet = pgInfo.save()
    else:
        msg = 'pgInfo save error'
        return Response(msg, status=status.HTTP_202_ACCEPTED)

    test_record_data = {
        'pg_info': pgInfoRet.id,
        'linux_info': linuxInfoRet.id,
        'meta_info': metaInfoRet.id,
        'test_machine_id': 1,
        'test_desc': 'here is desc',
        'meta_time': metaInfoRet.date
    }
    testRecord = CreateTestRecordSerializer(data=test_record_data)
    testRecordRet = None
    if testRecord.is_valid():
        testRecordRet = testRecord.save()
    else:
        msg = 'testRecord save error'
        return Response(msg, status=status.HTTP_202_ACCEPTED)

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
                print 'std is:'+ str(dataset['std'])

                test_dataset_data = {
                    'test_record': testRecordRet.id,
                    'clients': client_num,
                    'scale': scale,
                    'std': dataset['std'],
                    'metric': dataset['metric'],
                    'median': dataset['median'],
                    'test_cate': test_cate.id,
                    # status,percentage cal by tarr
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
                    msg = 'testDateSet save error'
                    return Response(msg, status=status.HTTP_202_ACCEPTED)




    msg = 'upload success'
    return Response(msg, status=status.HTTP_201_CREATED)
