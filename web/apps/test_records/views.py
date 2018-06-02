# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .serializer import TestRecordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import TestRecord
# Create your views here.
class TestRecordListView(APIView):
    """
    List all records, or create a new record.
    """
    def get(self, request, format=None):
        testRecords = TestRecord.objects.all()
        records_serializer = TestRecordSerializer(testRecords, many=True)
        return Response(records_serializer.data)

    def post(self, request, format=None):
        serializer = TestRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)