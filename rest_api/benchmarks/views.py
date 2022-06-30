import json
from math import ceil

from django.http import JsonResponse
from django.shortcuts import render
from benchmarks.models import PgBenchBenchmark, PgBenchResult, PgBenchStatement, PgBenchRunStatement, PgBenchLog, PgStatStatements, PgStatStatementsQuery, CollectdCpu, CollectdProcess, CollectdContextswitch, CollectdIpcShm, CollectdIpcMsg, CollectdIpcSem, CollectdMemory, CollectdSwap, CollectdVmem, CollectdDisk
from runs.models import RunInfo
from machines.models import Machine

def pgbench_benchmark_view(request):

    benchmarks = PgBenchBenchmark.objects.all().values()
    benchmarks_list = list(benchmarks)

    return JsonResponse(benchmarks_list, safe=False)


def pgbench_result_complete_view(request, id):
    results = PgBenchResult.objects.filter(pgbench_result_id=id).order_by('-pgbench_result_id').values('pgbench_result_id', 'tps', 'latency', 'mode', 'start', 'end', 'iteration', 'init', 'benchmark_config', 'run_id_id', 'run_id_id__machine_id', 'run_id_id__machine_id__machine_type', 'run_id_id__machine_id__alias', 'run_id_id__os_version_id__dist_id_id__dist_name', 'run_id_id__os_version_id__release', 'run_id_id__git_branch_id__name', 'run_id_id__git_commit', 'run_id_id__os_kernel_version_id_id__kernel_id__kernel_name', 'run_id_id__os_kernel_version_id__kernel_release')
    results_list = list(results)

    logs = PgBenchLog.objects.filter(pgbench_result_id=results_list[0]['pgbench_result_id']).values()
    run_statements = PgBenchRunStatement.objects.filter(pgbench_result_id=results_list[0]['pgbench_result_id']).values('line_id', 'latency', 'pgbench_run_statement_id', 'result_id')
    config = PgBenchBenchmark.objects.filter(pgbench_benchmark_id=results_list[0]['benchmark_config']).values()
    pg_stat_statements = PgStatStatements.objects.filter(pgbench_result_id=results_list[0]['pgbench_result_id']).values()
    collectd_cpu = CollectdCpu.objects.filter(pgbench_result_id=results_list[0]['pgbench_result_id']).values()
    collectd_process = CollectdProcess.objects.filter(pgbench_result_id=results_list[0]['pgbench_result_id']).values()
    collectd_contextswitch = CollectdContextswitch.objects.filter(pgbench_result_id=results_list[0]['pgbench_result_id']).values()
    collectd_ipc_shm = CollectdIpcShm.objects.filter(pgbench_result_id=results_list[0]['pgbench_result_id']).values()
    collectd_ipc_msg = CollectdIpcMsg.objects.filter(pgbench_result_id=results_list[0]['pgbench_result_id']).values()
    collectd_ipc_sem = CollectdIpcSem.objects.filter(pgbench_result_id=results_list[0]['pgbench_result_id']).values()
    collectd_memory = CollectdMemory.objects.filter(pgbench_result_id=results_list[0]['pgbench_result_id']).values()
    collectd_swap = CollectdSwap.objects.filter(pgbench_result_id=results_list[0]['pgbench_result_id']).values()
    collectd_vmem = CollectdVmem.objects.filter(pgbench_result_id=results_list[0]['pgbench_result_id']).values()
    collectd_disk = CollectdDisk.objects.filter(pgbench_result_id=results_list[0]['pgbench_result_id']).values()

    logs_list = list(logs)
    run_statements_list = list(run_statements)
    config_list = list(config)
    pg_stat_statements_list = list(pg_stat_statements)
    collectd_cpu_list = list(collectd_cpu)
    collectd_process_list = list(collectd_process)
    collectd_contextswitch_list = list(collectd_contextswitch)
    collectd_ipc_shm_list = list(collectd_ipc_shm)
    collectd_ipc_msg_list = list(collectd_ipc_msg)
    collectd_ipc_sem_list = list(collectd_ipc_sem)
    collectd_memory_list = list(collectd_memory)
    collectd_swap_list = list(collectd_swap)
    collectd_vmem_list = list(collectd_vmem)
    collectd_disk_list = list(collectd_disk)

    for run_statement in run_statements_list:
        statements = PgBenchStatement.objects.filter(pgbench_statement_id=run_statement['result_id']).values()
        statements_list = list(statements)
        run_statement['statements'] = statements_list

    for pg_stat_statements in pg_stat_statements_list:
        query = PgStatStatementsQuery.objects.filter(query_id=pg_stat_statements['query_id']).values().first()['query']
        pg_stat_statements['query'] = query

    collectd = {
        'cpu': collectd_cpu_list,
        'process': collectd_process_list,
        'contextswitch': collectd_contextswitch_list,
        'ipc_shm': collectd_ipc_shm_list,
        'ipc_msg': collectd_ipc_msg_list,
        'ipc_sem': collectd_ipc_sem_list,
        'memory': collectd_memory_list,
        'swap': collectd_swap_list,
        'vmem': collectd_vmem_list,
        'disk': collectd_disk_list
    }

    results_list[0]['pgbench_log'] = logs_list
    results_list[0]['pgbench_run_statement'] = run_statements_list
    results_list[0]['benchmark_config'] = config_list
    results_list[0]['pg_stat_statements'] = pg_stat_statements_list
    results_list[0]['collectd'] = collectd

    return render(request, 'benchmarks/complete_result.html', {'results': results_list})


def postgres_history_view(request, machine):
    print("hit!")
    history = Machine.objects.raw("with a as (select p1.machine_id_id, p1.name, p1.db_settings_id_id settings1, p2.db_settings_id_id settings2, p1.setting_name, p1.setting_value value1, p1.setting_unit unit1, p2.setting_value value2, p2.setting_unit unit2 from (select * from postgres_postgressettings, runs_runinfo, runs_branch, machines_machine where postgres_postgressettings.db_settings_id_id = runs_runinfo.postgres_info_id and runs_branch.branch_id = runs_runinfo.git_branch_id and machines_machine.machine_id = runs_runinfo.machine_id_id and machine_id_id = %s) p1, (select * from postgres_postgressettings, runs_runinfo, runs_branch, machines_machine where postgres_postgressettings.db_settings_id_id = runs_runinfo.postgres_info_id and runs_branch.branch_id = runs_runinfo.git_branch_id and machines_machine.machine_id = runs_runinfo.machine_id_id and machine_id_id = %s) p2 where p1.db_settings_id_id < p2.db_settings_id_id and p1.setting_name = p2.setting_name and p1.name = p2.name and (p1.setting_value <> p2.setting_value or p1.setting_unit <> p2.setting_unit)), b as (select machine_id, alias, machine_type, kernel_name, name, min(run_id), min(runs_runinfo.add_time) add_time, postgres_info_id from machines_machine, runs_runinfo, runs_branch, systems_oskernelversion, systems_kernel where runs_runinfo.machine_id_id = machines_machine.machine_id and runs_runinfo.git_branch_id = runs_branch.branch_id and runs_runinfo.os_kernel_version_id_id = systems_oskernelversion.os_kernel_version_id and systems_oskernelversion.kernel_id_id = systems_kernel.kernel_id and machine_id = %s group by name, postgres_info_id, machine_id, alias, machine_type, kernel_name order by name, min), c as (select postgres_info_id prev, lead(postgres_info_id) over(partition by name) as next from b) select distinct min, add_time, settings1, settings2, setting_name, unit1, unit2, value1, value2, b.machine_id, a.name, machine_type, alias, kernel_name, first_run, last_run, min_add_time, max_add_time from a, b, c, (select max(run_id) last_run, max(add_time) max_add_time from runs_runinfo where machine_id_id = %s) d, (select min(run_id) first_run, min(add_time) min_add_time from runs_runinfo where machine_id_id = %s) e where a.settings1 = c.prev and a.settings2 = c.next and a.settings2 = b.postgres_info_id order by min;", [machine, machine, machine, machine, machine])
    print(history)
    history_list = list()

    for row in history:
        print("inside for")
        print(row)
        machine = {}

        for column in history.columns:
            machine[column] = getattr(row, column)

        history_list.append(machine)

    print(history_list)
    return JsonResponse(history_list, safe=False)


def overview_view(request):

    overview = PgBenchBenchmark.objects.raw("select * from (select max(run_id) last_run, max(runs_runinfo.add_time) last_run_time, count(distinct run_id) runs, count(distinct dist_name) os_count, count(distinct pgbench_result_id) results_count, count(distinct benchmark_config_id) configs, count(distinct name) branches, count(distinct git_repo_id) repos from runs_runinfo, runs_branch, systems_osversion, systems_osdistributor, benchmarks_pgbenchresult where runs_runinfo.git_branch_id = runs_branch.branch_id and runs_runinfo.os_version_id_id = systems_osversion.os_version_id and systems_osversion.dist_id_id = systems_osdistributor.os_distributor_id and benchmarks_pgbenchresult.run_id_id = runs_runinfo.run_id) t1, (select count(distinct machine_id) machines_count, count(distinct owner_id_id) users from machines_machine) t2, (select count(run_id) recent_runs from runs_runinfo where add_time > 'now'::timestamp - '1 month'::interval) t3, (select machine_id_id last_machine_id, alias last_machine_alias from machines_machine, runs_runinfo where runs_runinfo.machine_id_id = machines_machine.machine_id and run_id = (select max(run_id) from runs_runinfo)) t4, (select * from (select machine_id_id, pgbench_benchmark_id, count(pgbench_result_id), scale, clients, duration, read_only from runs_runinfo, benchmarks_pgbenchresult, benchmarks_pgbenchbenchmark where runs_runinfo.run_id = benchmarks_pgbenchresult.run_id_id and benchmarks_pgbenchresult.benchmark_config_id = benchmarks_pgbenchbenchmark.pgbench_benchmark_id group by machine_id_id, pgbench_benchmark_id, scale, clients, duration, read_only) tmp where count = (select max(count) from (select machine_id_id, pgbench_benchmark_id, count(pgbench_result_id), scale, clients, duration, read_only from runs_runinfo, benchmarks_pgbenchresult, benchmarks_pgbenchbenchmark where runs_runinfo.run_id = benchmarks_pgbenchresult.run_id_id and benchmarks_pgbenchresult.benchmark_config_id = benchmarks_pgbenchbenchmark.pgbench_benchmark_id group by machine_id_id, pgbench_benchmark_id, scale, clients, duration, read_only) tmp) limit 1) t5;")

    overview_list = []
    overview_json = {}

    for row in overview:
        for column in overview.columns:
            overview_json[column] = getattr(row, column)

    overview_list.append(overview_json)

    return JsonResponse(overview_list, safe=False)


def pgbench_benchmark_machines_view(request):

    benchmarks_machines = PgBenchBenchmark.objects.raw("select pgbench_benchmark_id, scale, duration, read_only, clients, machine_id, alias, machines_machine.description, machines_machine.add_time, machine_type, username, count(pgbench_benchmark_id) from benchmarks_pgbenchbenchmark, benchmarks_pgbenchresult, runs_runinfo, machines_machine, auth_user where benchmarks_pgbenchbenchmark.pgbench_benchmark_id = benchmarks_pgbenchresult.benchmark_config_id and benchmarks_pgbenchresult.run_id_id = runs_runinfo.run_id and runs_runinfo.machine_id_id = machines_machine.machine_id and machines_machine.owner_id_id = auth_user.id group by machine_id, alias, machines_machine.description, machines_machine.add_time, machine_type, username, pgbench_benchmark_id, scale, duration, read_only, clients;")
    benchmarks_machines_list = []

    for row in benchmarks_machines:
        benchmark_machine = {}
        for column in benchmarks_machines.columns:
            benchmark_machine[column] = getattr(row, column)
        benchmarks_machines_list.append(benchmark_machine)

    machines = {}
    benchmarks = 0
    for bm in benchmarks_machines_list:
        read_only = 'read-write test'
        if bm['read_only']:
            read_only = 'read-only test'
        benchmark = 'Scale ' + str(bm['scale']) + ', Duration ' + str(bm['duration']) + ', Clients ' + str(bm['clients']) + ', ' + read_only
        machine = {
            'alias': bm['alias'],
            'add_time': str(bm['add_time'])[:10],
            'type': bm['machine_type'],
            'owner': bm['username'],
            'count': bm['count'],
            'config_id': bm['pgbench_benchmark_id'],
            'id': bm['machine_id'],
        }
        if benchmark not in machines:
            machines[benchmark] = []
            benchmarks += 1
        machines[benchmark].append(machine)
    return render(request, 'benchmarks/index.html', {'machines': machines})


def machine_history_view(request, machine):

    machine_history = Machine.objects.raw("select machine_id, alias, machines_machine.description, machines_machine.add_time, machine_type, username, email, url, dist_name, kernel_name, kernel_release, kernel_version, release, codename, compiler, name, url, min(run_id) as run_id, count(run_id), postgres_info_id, mounts, systems_hardwareinfo.sysctl, runs_runinfo.hardware_info_id, pgbench_benchmark_id, scale, duration, read_only, clients, cpu_brand, hz, cpu_cores, total_memory, total_swap from runs_gitrepo, benchmarks_pgbenchbenchmark, benchmarks_pgbenchresult, runs_runinfo, runs_branch, machines_machine, auth_user, systems_compiler, systems_oskernelversion, systems_kernel, systems_osdistributor, systems_osversion, systems_hardwareinfo where benchmarks_pgbenchbenchmark.pgbench_benchmark_id = benchmarks_pgbenchresult.benchmark_config_id and runs_branch.git_repo_id = runs_gitrepo.git_repo_id and benchmarks_pgbenchresult.run_id_id = runs_runinfo.run_id and runs_runinfo.git_branch_id = runs_branch.branch_id and systems_hardwareinfo.hardware_info_id = runs_runinfo.hardware_info_id and runs_runinfo.machine_id_id = machines_machine.machine_id and runs_runinfo.compiler_id = systems_compiler.compiler_id and machines_machine.owner_id_id = auth_user.id and runs_runinfo.os_version_id_id = systems_osversion.os_version_id and runs_runinfo.os_kernel_version_id_id = systems_oskernelversion.os_kernel_version_id and systems_oskernelversion.kernel_id_id = systems_kernel.kernel_id and systems_osversion.dist_id_id = systems_osdistributor.os_distributor_id and machine_id_id = %s group by url, dist_name, machines_machine.add_time, kernel_name, kernel_release, kernel_version, release, codename, mounts, systems_hardwareinfo.sysctl, compiler, name, postgres_info_id, runs_runinfo.hardware_info_id, pgbench_benchmark_id, scale, duration, read_only, clients, machine_id, alias, machines_machine.description, machine_type, username, email, cpu_brand, hz, cpu_cores, total_memory, total_swap order by run_id desc;", [machine])

    machine_history_list = []

    for row in machine_history:

        machine = {}

        for column in machine_history.columns:
            machine[column] = getattr(row, column)

        machine_history_list.append(machine)
    # print(machine_history_list)
    reports = 0
    benchmarks = {}
    compiler_data = []
    os_data = []
    branches = []
    sysctl_data = []
    for history in machine_history_list:
        history['total_memory'] = '%s GB' % ceil(history['total_memory'] / 1073741824)
        history['total_swap'] = '%s GB' % ceil(history['total_swap'] / 1073741824)
        def comapre_call_back(item, compared_str, item_name):
            return item[item_name] == compared_str
        if not compiler_data:
            compiler_data.append({'compiler': history['compiler'], 'run_id': history['run_id']})
        elif not any(comapre_call_back(item, history['compiler'], 'compiler') for item in compiler_data):
            compiler_data.append({'compiler': history['compiler'], 'run_id': history['run_id']})
        reports += history['count']
        read_only = 'read-write test'
        if history['read_only']:
            read_only = 'read-only test'
        benchmark = 'Scale ' + str(history['scale']) + ', Duration ' + str(history['duration']) + ', Clients ' + str(
            history['clients']) + ', ' + read_only
        benchmarks[history['pgbench_benchmark_id']] = benchmark
        os_string = history['kernel_name'] + ' ' + history['dist_name'] + ' ' + history['release'] + ' (' + \
                    history['codename'] + ') ' + history['kernel_release'] + ' ' + history['kernel_version']
        if not os_data:
            os_data.append({'os': os_string, 'run_id': history['run_id']})
        elif not any(comapre_call_back(item, os_string, 'os') for item in os_data):
            os_data.append({'os': os_string, 'run_id': history['run_id']})
        if history['name'] not in branches:
            branches.append(history['name'])
        sysctl_object = json.loads(history['sysctl'])
        # print('*******************', sysctl_object)
        sysctl_string = ''
        if sysctl_object:
            for key, value in sysctl_object.items():
                sysctl_string += key + ' = ' + value + '\n'
            pass
            if not sysctl_data:
                sysctl_data.append({
                    'sysctl': sysctl_string,
                    'run_id': history['run_id']
                })
            elif not any(comapre_call_back(item, sysctl_string, 'sysctl') for item in sysctl_data):
                sysctl_data.append({
                    'sysctl': sysctl_string,
                    'run_id': history['run_id']
                })
    configurationListContent = ''
    for key, value in benchmarks.items():
        configurationListContent += '<div><a href="/trend?id=${id}&config=${value}"> ${name}</a></div>' % ()

    return render(request, 'machines/machine_history.html', {'machine_history_list': machine_history_list,
                                                             'reports': reports,
                                                             'benchmarks': benchmarks,
                                                             'branches': branches,
                                                             'sysctl_data': sysctl_data,
                                                             'compiler_data': compiler_data,
                                                             'os_data': os_data
                                                             })


def pgbench_runs_view(request, commit, machine, config):

    commit = '%' + commit

    pgbench_runs = RunInfo.objects.raw("select runs_runinfo.run_id, pgbench_result_id, runs_runinfo.add_time from benchmarks_pgbenchbenchmark, benchmarks_pgbenchresult, runs_runinfo, runs_branch where runs_runinfo.git_branch_id = runs_branch.branch_id and benchmarks_pgbenchbenchmark.pgbench_benchmark_id = benchmarks_pgbenchresult.benchmark_config_id and benchmarks_pgbenchresult.run_id_id = runs_runinfo.run_id and git_commit like %s and machine_id_id = %s and benchmark_config_id = %s and runs_branch.git_repo_id < 5 order by add_time;", [commit, machine, config])

    pgbench_runs_list = []

    for row in pgbench_runs:
        pgbench_run = {}

        for column in pgbench_runs.columns:
            pgbench_run[column] = getattr(row, column)

        pgbench_runs_list.append(pgbench_run)

    return JsonResponse(pgbench_runs_list, safe=False)


def pgbench_benchmark_trend_view(request, machine, config):

    pgbench_trends = PgBenchBenchmark.objects.raw("select avg(tps) as avgtps, avg(latency) as avglat, stddev(tps) as stdtps, stddev(latency) as stdlat, min(tps) as mintps, min(latency) as minlat, max(tps) as maxtps, max(latency) as maxlat, min(runs_runinfo.add_time) as add_time, count(git_commit), git_commit, pgbench_benchmark_id, name, scale, duration, read_only, clients, machine_id, alias, machines_machine.description, machine_type, username, email, url, min(dist_name) as dist_name, min(kernel_name) as kernel_name, max(systems_compiler.compiler) as compiler from benchmarks_pgbenchbenchmark, benchmarks_pgbenchresult, runs_gitrepo, runs_runinfo, runs_branch, machines_machine, auth_user, systems_compiler, systems_oskernelversion, systems_kernel, systems_osdistributor, systems_osversion where benchmarks_pgbenchbenchmark.pgbench_benchmark_id = benchmarks_pgbenchresult.benchmark_config_id and runs_branch.git_repo_id = runs_gitrepo.git_repo_id and benchmarks_pgbenchresult.run_id_id = runs_runinfo.run_id and runs_runinfo.git_branch_id = runs_branch.branch_id and runs_runinfo.machine_id_id = machines_machine.machine_id and runs_runinfo.compiler_id = systems_compiler.compiler_id and machines_machine.owner_id_id = auth_user.id and runs_runinfo.os_version_id_id = systems_osversion.os_version_id and runs_runinfo.os_kernel_version_id_id = systems_oskernelversion.os_kernel_version_id and systems_oskernelversion.kernel_id_id = systems_kernel.kernel_id and systems_osversion.dist_id_id = systems_osdistributor.os_distributor_id and machine_id_id = %s and benchmark_config_id = %s and runs_branch.git_repo_id < 5 group by git_commit, name, pgbench_benchmark_id, url, machine_id, alias, machines_machine.description, machine_type, username, email,scale, duration, read_only, clients order by add_time desc;", [machine, config])

    pgbench_trends_list = []

    for row in pgbench_trends:
        pgbench_trend = {}

        for column in pgbench_trends.columns:
            pgbench_trend[column] = getattr(row, column)

        pgbench_trends_list.append(pgbench_trend)

    return JsonResponse(pgbench_trends_list, safe=False)
