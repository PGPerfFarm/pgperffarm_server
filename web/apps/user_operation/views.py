# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import mixins, viewsets, permissions, status

from rest_framework import authentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from util.response import PGJsonResponse
from users.models import UserMachine, UserProfile
from serializer import UserMachineManageSerializer, UserPortalInfoSerializer


class UserMachineListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    List test records
    """
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    permission_classes = (permissions.IsAuthenticated, )
    queryset = UserMachine.objects.all().order_by('add_time')
    serializer_class = UserMachineManageSerializer
    # pagination_class = StandardResultsSetPagination

class UserPortalInfoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
     user info
    """
    # authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    # permission_classes = (permissions.IsAuthenticated, )
    queryset = UserProfile.objects.all().order_by('date_joined')
    serializer_class = UserPortalInfoSerializer

class UserMachinePermission(permissions.BasePermission):
    """
    Machine upload permission check
    """

    def has_permission(self, request, view):
        secret = request.data.secret
        ret = UserMachine.objects.filter(machine_secret=secret, is_active=1).exists()
        return ret
