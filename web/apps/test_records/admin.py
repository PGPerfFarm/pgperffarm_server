# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import TestRecord, TestBranch

class TestRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'branch', 'uuid', 'test_machine')
    list_filter = ('branch',)
    actions = ['approve_machine']

admin.site.register(TestRecord, TestRecordAdmin)

admin.site.register(TestBranch)