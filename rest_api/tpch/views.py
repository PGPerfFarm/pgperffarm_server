from django.shortcuts import render

# Create your views here.
import json
import os
import sys
from datetime import datetime
from math import ceil
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from benchmarks.models import PgBenchBenchmark
from machines.models import Machine
from tpch.models import Run


def index(request):
    benchmarks = PgBenchBenchmark.objects.all().values()
    benchmarks_list = list(benchmarks)

    return render(request, 'benchmarks/tpch.html', {'result': benchmarks_list})


@csrf_exempt
def create_tpch_run(request, format=None):
    print("hit")
    error = ''
    machine = None

    data = json.loads(request.body)
    json_data = data[0]

    if sys.getsizeof(json_data) > 10000:
        error = 'The result size is too big.'
        raise RuntimeError(error)

    from django.db import transaction

    # check if machine exists
    try:
        secret = request.META.get("HTTP_AUTHORIZATION")
        print(secret)
        try:
            machine = Machine.objects.filter(machine_secret=secret).get()

            if machine.approved == False:
                error = 'The machine is not approved.'
                raise RuntimeError(error)

        except Machine.DoesNotExist:
            error = "The machine is unavailable"
            raise RuntimeError(error)

        print("got machine")
        print(machine)
        with transaction.atomic():

            run = Run(
                machine_id=machine,
                scale_factor=json_data['scale_factor'],
                date_submitted=json_data['date_submitted'],
                QphH=json_data['qphh_size'],
            )

            try:
                run.save()

            except Exception as e:

                raise RuntimeError(e)

    except Exception as e:

        if error == '':
            error = e

        try:
            print('error: %s' % error)

        except Exception as e:

            with open(os.path.join(sys.path[0], "log.txt"), "a+") as f:
                error_string = str(datetime.now()) + ' ' + str(error)
                f.write(error_string)

        return HttpResponse(status=406)

    print('Upload successful!')
    return HttpResponse(status=201)
