# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination

from .serializer import TestRecordSerializer, TestRecordDetailSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from .models import TestRecord

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

    # def byteify(input):
    #     if isinstance(input, dict):
    #         return {byteify(key): byteify(value) for key, value in input.iteritems()}
    #     elif isinstance(input, list):
    #         return [byteify(element) for element in input]
    #     elif isinstance(input, unicode):
    #         return input.encode('utf-8')
    #     else:
    #         return input
    return Response((data), status=status.HTTP_200_OK)
