# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from rest_framework import mixins, viewsets, permissions

from rest_framework import authentication
from rest_framework.pagination import PageNumberPagination
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .filters import MachineRecordListFilter, UserMachineListFilter
from test_records.models import TestRecord
from users.models import UserMachine, UserProfile
from users.serializer import CreateUserProfileSerializer
from .serializer import UserMachineManageSerializer, UserPortalInfoSerializer, TestRecordListSerializer, \
    UserMachineSerializer, CreateUserMachineSerializer
from rest_framework.response import Response
from rest_framework import status

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class MiddleResultsSetPagination(PageNumberPagination):
    page_size = 40
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserMachineRecordByBranchListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    List machine records by branch
    """

    queryset = TestRecord.objects.all().order_by('-add_time')
    serializer_class = TestRecordListSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = MachineRecordListFilter

class UserMachineListViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    List test records
    """
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    permission_classes = (permissions.IsAuthenticated, )
    queryset = UserMachine.objects.all().order_by('add_time')
    serializer_class = UserMachineManageSerializer
    pagination_class = MiddleResultsSetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = UserMachineListFilter

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = {}
        data['os_name'] = request.data['os_name']
        data['os_version'] = request.data['os_version']
        data['comp_name'] = request.data['comp_name']
        data['comp_version'] = request.data['comp_version']

        username = request.data['machine_owner']
        user = UserProfile.objects.filter(username=username).filter().first()
        user_serializer = CreateUserProfileSerializer(user)

        data['machine_owner'] = user_serializer.data['id']

        serializer = CreateUserMachineSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        machine = self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response('success', status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class PublicMachineListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    List all machines
    """
    queryset = UserMachine.objects.all().order_by('add_time')
    serializer_class = UserMachineManageSerializer
    pagination_class = MiddleResultsSetPagination

class UserPortalInfoViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
     user info
    """
    # authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    # permission_classes = (permissions.IsAuthenticated, )
    lookup_field = 'username'
    queryset = UserProfile.objects.all()
    serializer_class = UserPortalInfoSerializer

class UserMachinePermission(permissions.BasePermission):
    """
    Machine upload permission check
    """

    def has_permission(self, request, view):
        secret = request.META.get("HTTP_AUTHORIZATION")
        # print(secret)
        # alias = request.data.alias
        ret = UserMachine.objects.filter(machine_secret=secret, state=1).exists()
        return ret
