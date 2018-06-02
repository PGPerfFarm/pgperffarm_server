# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import TestRecord
# Create your views here.
class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        testRecord = TestRecord.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)