from django.shortcuts import render

# Create your views here.
import json
from math import ceil

from django.http import JsonResponse
from django.shortcuts import render
from benchmarks.models import PgBenchBenchmark


def index(request):

    benchmarks = PgBenchBenchmark.objects.all().values()
    benchmarks_list = list(benchmarks)

    return render(request, 'benchmarks/tpch.html', {'result': benchmarks_list})