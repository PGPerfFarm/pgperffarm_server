# -*- coding: utf-8 -*-
import django_filters
from django.db.models import Q

from records.models import TestRecord


class TestRecordListFilter(django_filters.rest_framework.FilterSet):
    """
    TestRecordListFilter
    """
    date = django_filters.DateTimeFilter(name='add_time',lookup_expr='gt')
    branch = django_filters.CharFilter(name='branch__branch_name')
    class Meta:
        model = TestRecord
        fields = ['date', 'branch']