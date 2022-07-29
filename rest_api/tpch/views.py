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
from machines.models import Machine
from tpch.models import Run


def index(request):
    tpch_runs = Run.objects.raw('select machines_machine.machine_id, machines_machine.alias, tpch_run.run_id, tpch_run.date_submitted, tpch_run.scale_factor, tpch_run.power_score, tpch_run.throughput_score, tpch_run.composite_score from tpch_run, machines_machine where tpch_run.machine_id = machines_machine.machine_id')
    tpch_runs = list(tpch_runs)
    print(tpch_runs)
    return render(request, 'benchmarks/tpch.html', {'result': tpch_runs})


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
        try:
            machine = Machine.objects.filter(machine_secret=secret).get()

            if machine.approved == False:
                error = 'The machine is not approved.'
                raise RuntimeError(error)

        except Machine.DoesNotExist:
            error = "The machine is unavailable"
            raise RuntimeError(error)

        with transaction.atomic():

            run = Run(
                machine=machine,
                scale_factor=json_data['scale_factor'],
                date_submitted=json_data['date_submitted'],
                composite_score=json_data['qphh_size'],
                power_score=json_data['power_size'],
                throughput_score=json_data['throughput_size'],
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
