# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

# Create your views here.
from rest_framework import permissions

from .models import UserProfile, UserMachine


class CustomBackend(ModelBackend):
    """
    custom user auth
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username))
            if user.check_password(password):
                return user


        except Exception as e:
            return None


class UserMachinePermission(permissions.BasePermission):
    """
    Machine permission check
    """

    def has_permission(self, request, view):
        secret = request.data.secret
        ret = UserMachine.objects.filter(machine_secret=secret,is_active=1).exists()
        return ret
