# -*- coding: utf-8 -*-
from django.views.generic.base import View

class TestListView(View):
    def get(self, request):

        json_list = []
        # testRecords = TestRecord.objects.all();
        testRecords = [1, 2]

        from django.forms.models import model_to_dict

        import json
        from django.core import serializers
        json_data = serializers.serialize('json', testRecords)
        json_data = json.loads(json_data)
        from django.http import HttpResponse, JsonResponse

        return JsonResponse(json_data, safe=False)