
# -*- coding: utf-8 -*-
import django_filters
from django.db.models import Q

from .models import TestRecord


class TestRecordListFilter(django_filters.rest_framework.FilterSet):
    """
    TestRecordListFilter
    """
    date = django_filters.DateTimeFilter(name='add_time',lookup_expr='gt')

    class Meta:
        model = TestRecord
        fields = ['date', ]