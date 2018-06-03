# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination

from .serializer import TestRecordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from .models import TestRecord

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class TestRecordListViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    List all records in status page, or create a new record.
    """
    queryset = TestRecord.objects.all()
    serializer_class = TestRecordSerializer
    pagination_class = StandardResultsSetPagination
    # authentication_classes = None
    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    # def get(self, request, format=None):
    #     testRecords = TestRecord.objects.all()
    #     records_serializer = TestRecordSerializer(testRecords, many=True)
    #     return Response(records_serializer.data)
    #
    # def post(self, request, format=None):
    #     serializer = TestRecordSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
