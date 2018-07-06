# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import mixins, viewsets, permissions

from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from models import UserMachine
from serializer import UserMachineManageSerializer


class UserMachineListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    List test records
    """
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    queryset = UserMachine.objects.all().order_by('add_time')
    serializer_class = UserMachineManageSerializer
    # pagination_class = StandardResultsSetPagination

class UserMachinePermission(permissions.BasePermission):
    """
    Machine permission check
    """

    def has_permission(self, request, view):
        secret = request.data.secret
        ret = UserMachine.objects.filter(machine_secret=secret,is_active=1).exists()
        return ret