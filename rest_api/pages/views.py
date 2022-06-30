from django.shortcuts import render

from benchmarks.models import PgBenchBenchmark


def index(request):
    overview = PgBenchBenchmark.objects.raw("select * from (select max(run_id) last_run, max(runs_runinfo.add_time) last_run_time, count(distinct run_id) runs, count(distinct dist_name) os_count, count(distinct pgbench_result_id) results_count, count(distinct benchmark_config_id) configs, count(distinct name) branches, count(distinct git_repo_id) repos from runs_runinfo, runs_branch, systems_osversion, systems_osdistributor, benchmarks_pgbenchresult where runs_runinfo.git_branch_id = runs_branch.branch_id and runs_runinfo.os_version_id_id = systems_osversion.os_version_id and systems_osversion.dist_id_id = systems_osdistributor.os_distributor_id and benchmarks_pgbenchresult.run_id_id = runs_runinfo.run_id) t1, (select count(distinct machine_id) machines_count, count(distinct owner_id_id) users from machines_machine) t2, (select count(run_id) recent_runs from runs_runinfo where add_time > 'now'::timestamp - '1 month'::interval) t3, (select machine_id_id last_machine_id, alias last_machine_alias from machines_machine, runs_runinfo where runs_runinfo.machine_id_id = machines_machine.machine_id and run_id = (select max(run_id) from runs_runinfo)) t4, (select * from (select machine_id_id, pgbench_benchmark_id, count(pgbench_result_id), scale, clients, duration, read_only from runs_runinfo, benchmarks_pgbenchresult, benchmarks_pgbenchbenchmark where runs_runinfo.run_id = benchmarks_pgbenchresult.run_id_id and benchmarks_pgbenchresult.benchmark_config_id = benchmarks_pgbenchbenchmark.pgbench_benchmark_id group by machine_id_id, pgbench_benchmark_id, scale, clients, duration, read_only) tmp where count = (select max(count) from (select machine_id_id, pgbench_benchmark_id, count(pgbench_result_id), scale, clients, duration, read_only from runs_runinfo, benchmarks_pgbenchresult, benchmarks_pgbenchbenchmark where runs_runinfo.run_id = benchmarks_pgbenchresult.run_id_id and benchmarks_pgbenchresult.benchmark_config_id = benchmarks_pgbenchbenchmark.pgbench_benchmark_id group by machine_id_id, pgbench_benchmark_id, scale, clients, duration, read_only) tmp) limit 1) t5;")
    overview_json = {}
    for row in overview:
        for column in overview.columns:
            overview_json[column] = getattr(row, column)
    # print(overview_json)
    return render(request, 'pages/index.html', {'result': overview_json})
