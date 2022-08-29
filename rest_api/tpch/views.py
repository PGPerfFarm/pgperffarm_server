from django.http import JsonResponse
from django.shortcuts import render
from machines.models import Machine
from runs.models import Branch
from tpch.models import TpchResult, TpchQueryResult


def index(request):
    scale_groups = Machine.objects.raw("select machines_machine.machine_id, auth_user.username, Count(tpch_tpchresult.id), tpch_tpchconfig.scale_factor, machines_machine.alias, Max(runs_runinfo.add_time) last_run_time from tpch_tpchresult, tpch_tpchconfig, runs_runinfo, auth_user, machines_machine where tpch_tpchresult.run_id_id = runs_runinfo.run_id AND runs_runinfo.machine_id_id = machines_machine.machine_id AND machines_machine.owner_id_id = auth_user.id AND tpch_tpchresult.benchmark_config_id = tpch_tpchconfig.id GROUP  BY auth_user.username, tpch_tpchconfig.scale_factor, machines_machine.machine_id, machines_machine.alias")
    scale_groups = list(scale_groups)
    overview_json = {}
    for scale_g in scale_groups:
        if scale_g.scale_factor not in overview_json:
            overview_json[scale_g.scale_factor] = [scale_g]
        else:
            overview_json[scale_g.scale_factor].append(scale_g)
    return render(request, 'benchmarks/tpch.html', {'overview_json': overview_json})


def trend(request, machine, scale):
    tpch_trends = Branch.objects.raw('select machines_machine.alias, auth_user.username, runs_branch.branch_id, tpch_tpchresult.git_commit, tpch_tpchresult.scale_factor, tpch_tpchresult.streams, runs_branch.name, tpch_tpchresult.machine_id, max(power_score) max_power_score, min(power_score) min_power_score, avg(power_score) ave_power_score, max(throughput_score) max_throughput_score, min(throughput_score) min_throughput_score, avg(throughput_score) ave_throughput_score, max(composite_score) max_composite_score, min(composite_score) min_composite_score, avg(composite_score) ave_composite_score from auth_user, tpch_tpchresult, runs_branch, machines_machine where auth_user.id = machines_machine.owner_id_id AND tpch_tpchresult.machine_id = machines_machine.machine_id AND runs_branch.branch_id = tpch_tpchresult.git_branch_id AND tpch_tpchresult.machine_id = %s AND tpch_tpchresult.scale_factor = %s group by auth_user.username, tpch_tpchresult.git_commit, tpch_tpchresult.scale_factor, tpch_tpchresult.streams, runs_branch.name, tpch_tpchresult.machine_id, runs_branch.branch_id, machines_machine.alias', (machine, scale))
    tpch_trends_list = []

    for row in tpch_trends:
        pgbench_trend = {}
        for column in tpch_trends.columns:
            pgbench_trend[column] = getattr(row, column)
        tpch_trends_list.append(pgbench_trend)

    return render(request, 'benchmarks/tpch_trend.html', {'tpch_trends_list': tpch_trends_list})


def details(request, id):
    tpch_runs = TpchResult.objects.raw(
        'select machines_machine.machine_id, machines_machine.alias, tpch_tpchresult.id, tpch_tpchresult.date_submitted, tpch_tpchresult.scale_factor, tpch_tpchresult.power_score, tpch_tpchresult.throughput_score, tpch_tpchresult.composite_score, tpch_tpchresult.git_commit, runs_branch.name from tpch_tpchresult, machines_machine, runs_branch where tpch_tpchresult.machine_id = machines_machine.machine_id and runs_branch.branch_id = tpch_tpchresult.git_branch_id and tpch_tpchresult.id = %s', [id])
    tpch_runs = list(tpch_runs)
    power_queries = TpchQueryResult.objects.raw("select id, query_idx, time from tpch_queryresult where tpch_queryresult.run_id = %s and type=%s", [id, 'power'])
    power_queries = list(power_queries)
    throughput_queries = TpchQueryResult.objects.raw("select id, query_idx, time from tpch_queryresult where tpch_queryresult.run_id = %s and type=%s", [id, 'throughput'])
    throughput_queries = list(throughput_queries)
    models = []
    for i in range(0, len(power_queries)):
        models.append({
            "model_name": power_queries[i].query_idx,
            "field1": power_queries[i].time,
            "field2": throughput_queries[i].time
        })
    return render(request, 'benchmarks/tpch_details.html', { 'id':id, 'models': models, 'result': tpch_runs})


def runs_commit_view(request, machine, scale, commit):
    commit = '%' + commit

    tpch_runs = TpchResult.objects.raw("select tpch_tpchresult.id, tpch_tpchresult.date_submitted from tpch_tpchresult, machines_machine where tpch_tpchresult.machine_id = machines_machine.machine_id AND tpch_tpchresult.machine_id = %s AND tpch_tpchresult.git_commit like %s AND tpch_tpchresult.scale_factor = %s order by tpch_tpchresult.date_submitted DESC", [machine, commit, scale])

    tpch_runs_list = []

    for row in tpch_runs:
        pgbench_run = {}

        for column in tpch_runs.columns:
            pgbench_run[column] = getattr(row, column)

        tpch_runs_list.append(pgbench_run)

    return JsonResponse(tpch_runs_list, safe=False)
