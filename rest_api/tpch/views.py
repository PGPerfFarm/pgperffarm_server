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
from runs.models import Branch
from tpch.models import Run, QueryResult


def index(request):
    tpch_runs = Run.objects.raw(
        'select machines_machine.machine_id, machines_machine.alias, tpch_run.id, tpch_run.date_submitted, tpch_run.scale_factor, tpch_run.power_score, tpch_run.throughput_score, tpch_run.composite_score from tpch_run, machines_machine where tpch_run.machine_id = machines_machine.machine_id')
    tpch_runs = list(tpch_runs)
    return render(request, 'benchmarks/tpch.html', {'result': tpch_runs})


def details(request, id):
    power_queries = QueryResult.objects.raw("select id, query_idx, time from tpch_queryresult where tpch_queryresult.run_id = %s and type=%s", [id, 'power'])
    power_queries = list(power_queries)
    throughput_queries = QueryResult.objects.raw("select id, query_idx, time from tpch_queryresult where tpch_queryresult.run_id = %s and type=%s", [id, 'throughput'])
    throughput_queries = list(throughput_queries)
    models = []
    for i in range(0, len(power_queries)):
        models.append({
            "model_name": power_queries[i].query_idx,
            "field1": power_queries[i].time,
            "field2": throughput_queries[i].time
        })
    return render(request, 'benchmarks/tpch_details.html', { 'id':id, 'models': models})


def save_tpch_query_result(res, phase, run):
    for k, v in res.items():
        query = QueryResult(
            query_idx=int(k),
            time=v,
            type=phase,
            run=run
        )
        query.save()


@csrf_exempt
def create_tpch_run(request, format=None):
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
            branch = Branch.objects.filter(name=json_data['branch']).get()
            new_run = Run.objects.create(machine=machine,
                                         scale_factor=json_data['scale_factor'],
                                         date_submitted=json_data['date_submitted'],
                                         composite_score=json_data['qphh_size'],
                                         power_score=json_data['power_size'],
                                         throughput_score=json_data['throughput_size'],
                                         git_commit=json_data['commit'],
                                         git_branch=branch, )
            try:
                save_tpch_query_result(json_data['power'], 'power', new_run)
                save_tpch_query_result(json_data['throughput'], 'throughput', new_run)
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
