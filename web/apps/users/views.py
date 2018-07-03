# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from models import UserProfile


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