import json
import os
import sys
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from email_notification.models import EmailNotification
from machines.models import Machine
from runs.models import Branch
from tpch.models import Run, QueryResult


def index(request):
    scale_groups = Machine.objects.raw("SELECT tpch_run.machine_id, auth_user.username, count(tpch_run.id), tpch_run.scale_factor, machines_machine.alias, Max(tpch_run.date_submitted) last_run_time FROM tpch_run, auth_user, machines_machine WHERE tpch_run.machine_id = machines_machine.machine_id AND auth_user.id = machines_machine.owner_id_id AND tpch_run.date_submitted > 'now'::timestamp - '1 month'::interval GROUP BY auth_user.username, tpch_run.scale_factor, tpch_run.machine_id, machines_machine.alias order by tpch_run.scale_factor DESC")
    scale_groups = list(scale_groups)
    overview_json = {}
    for scale_g in scale_groups:
        if scale_g.scale_factor not in overview_json:
            overview_json[scale_g.scale_factor] = [scale_g]
        else:
            overview_json[scale_g.scale_factor].append(scale_g)
    return render(request, 'benchmarks/tpch.html', {'overview_json': overview_json})


def trend(request, machine, scale):
    tpch_trends = Branch.objects.raw('select machines_machine.alias, auth_user.username, runs_branch.branch_id, tpch_run.git_commit, tpch_run.scale_factor, tpch_run.streams, runs_branch.name, tpch_run.machine_id, max(power_score) max_power_score, min(power_score) min_power_score, avg(power_score) ave_power_score, max(throughput_score) max_throughput_score, min(throughput_score) min_throughput_score, avg(throughput_score) ave_throughput_score, max(composite_score) max_composite_score, min(composite_score) min_composite_score, avg(composite_score) ave_composite_score from auth_user, tpch_run, runs_branch, machines_machine where auth_user.id = machines_machine.owner_id_id AND tpch_run.machine_id = machines_machine.machine_id AND runs_branch.branch_id = tpch_run.git_branch_id AND tpch_run.machine_id = %s AND tpch_run.scale_factor = %s group by auth_user.username, tpch_run.git_commit, tpch_run.scale_factor, tpch_run.streams, runs_branch.name, tpch_run.machine_id, runs_branch.branch_id, machines_machine.alias', (machine, scale))
    tpch_trends_list = []

    for row in tpch_trends:
        pgbench_trend = {}
        for column in tpch_trends.columns:
            pgbench_trend[column] = getattr(row, column)
        tpch_trends_list.append(pgbench_trend)

    return render(request, 'benchmarks/tpch_trend.html', {'tpch_trends_list': tpch_trends_list})


def details(request, id):
    tpch_runs = Run.objects.raw(
        'select machines_machine.machine_id, machines_machine.alias, tpch_run.id, tpch_run.date_submitted, tpch_run.scale_factor, tpch_run.power_score, tpch_run.throughput_score, tpch_run.composite_score, tpch_run.git_commit, runs_branch.name from tpch_run, machines_machine, runs_branch where tpch_run.machine_id = machines_machine.machine_id and runs_branch.branch_id = tpch_run.git_branch_id and tpch_run.id = %s', [id])
    tpch_runs = list(tpch_runs)
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
    return render(request, 'benchmarks/tpch_details.html', { 'id':id, 'models': models, 'result': tpch_runs})


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
                                         streams=json_data['streams'],
                                         date_submitted=json_data['date_submitted'],
                                         composite_score=json_data['qphh_size'],
                                         power_score=json_data['power_size'],
                                         throughput_score=json_data['throughput_size'],
                                         git_commit=json_data['commit'],
                                         git_branch=branch, )

            avg_same_config_result_raw = Machine.objects.raw(
                "select avg(composite_score) from tpch_run where scale_factor = %s and git_branch_id = %s and machine_id = %s group by git_branch_id",
                [new_run.scale_factor, new_run.git_branch.branch_id, new_run.machine_id.machine_id])
            avg_same_config_result = {}
            for row in avg_same_config_result_raw:
                for column in avg_same_config_result_raw.columns:
                    avg_same_config_result[column] = getattr(row, column)

            try:
                save_tpch_query_result(json_data['power'], 'power', new_run)
                save_tpch_query_result(json_data['throughput'], 'throughput', new_run)
            except Exception as e:

                raise RuntimeError(e)

        email_notification = EmailNotification.objects.get(owner=machine.owner_id, type=2)

        if avg_same_config_result and avg_same_config_result['avg_composite'] and email_notification.is_active and float(
                new_run.composite_score) < float(avg_same_config_result['avg_composite']) * (100 - email_notification.threshold) / 100:
            user = machine.owner_id
            from email_notification.utils import send_the_email
            message = "Dear " + user.username + "\n Your most recent TPC-H benchmark test (run id: %s) is %.2f" % (
            new_run.run_id, 1 - (float(new_run.composite_score) / float(
                avg_same_config_result['avgtps']))) + "% lower than the previous average."
            send_the_email(recipents=[user.email], subject="Performance Drop Alert —— Pgperffarm ", message=message)

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


def runs_commit_view(request, machine, scale, commit):
    commit = '%' + commit

    tpch_runs = Run.objects.raw("select tpch_run.id, tpch_run.date_submitted from tpch_run, machines_machine where tpch_run.machine_id = machines_machine.machine_id AND tpch_run.machine_id = %s AND tpch_run.git_commit like %s AND tpch_run.scale_factor = %s order by tpch_run.date_submitted DESC", [machine, commit, scale])

    tpch_runs_list = []

    for row in tpch_runs:
        pgbench_run = {}

        for column in tpch_runs.columns:
            pgbench_run[column] = getattr(row, column)

        tpch_runs_list.append(pgbench_run)

    return JsonResponse(tpch_runs_list, safe=False)
