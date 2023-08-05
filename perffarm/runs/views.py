import json
import sys
import os
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from runs.parsing_functions import parse_pgbench_options, parse_pgbench_results, parse_os_kernel, parse_compiler, \
    parse_git, parse_hardware, parse_postgres, parse_tpch_results ,parse_explain_results,parse_explain_results_costOff,parse_tpch_query_plans
from machines.models import Machine
from postgres.models import PostgresSettings
from runs.models import RunInfo, RunLog
from benchmarks.models import PgBenchBenchmark, PgBenchResult, BenchmarkType
from tpch.models import TpchConfig


def single_run_view(request, id):
    run = RunInfo.objects.filter(run_id=id).values('run_id', 'add_time', 'git_branch_id__name',
                                                   'git_branch_id__git_repo_id__url', 'git_commit',
                                                   'os_version_id__dist_id__dist_name', 'os_version_id__description',
                                                   'os_version_id__release', 'os_version_id__codename',
                                                   'os_kernel_version_id__kernel_release',
                                                   'os_kernel_version_id__kernel_version',
                                                   'os_kernel_version_id__kernel_id__kernel_name',
                                                   'compiler_id__compiler', 'machine_id', 'machine_id__alias',
                                                   'machine_id__machine_type', 'machine_id__description',
                                                   'machine_id__add_time', 'machine_id__owner_id__username',
                                                   'postgres_info_id', 'hardware_info_id__cpu_brand',
                                                   'hardware_info_id__hz', 'hardware_info_id__cpu_cores',
                                                   'hardware_info_id__total_memory', 'hardware_info_id__total_swap',
                                                   'hardware_info_id__mounts', 'hardware_info_id__sysctl')

    run_list = list(run)

    postgres_info = PostgresSettings.objects.filter(db_settings_id_id=run_list[0]['postgres_info_id']).values()
    postgres_info_list = list(postgres_info)

    pgbench_results = PgBenchResult.objects.filter(run_id_id=run_list[0]['run_id']).values()
    pgbench_results_list = list(pgbench_results)

    benchmarks = []
    for pgbench_result in pgbench_results_list:
        benchmark_config = PgBenchBenchmark.objects.filter(
            pgbench_benchmark_id=pgbench_result['benchmark_config_id']).values()
        benchmark_config_list = list(benchmark_config)
        read_only = 'read-write test'
        if benchmark_config_list[0]['read_only']:
            read_only = 'read-only test'
        config = 'Scale ' + str(benchmark_config_list[0]['scale']) + ', Duration ' + str(
            benchmark_config_list[0]['duration']) + ', Clients ' + str(
            benchmark_config_list[0]['clients']) + ', ' + read_only
        date = datetime.fromtimestamp(pgbench_result['start']).strftime('%Y-%m-%d %H:%M:%S')
        benchmarks.append({
            "config": config,
            "id": pgbench_result['pgbench_result_id'],
            "start": date,
        })

    return render(request, 'runs/index.html', {'run': run_list[0],
                                               'benchmarks': benchmarks,
                                               'postgres_info': postgres_info_list,
                                               })


@csrf_exempt
def create_run_info(request, format=None):
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

            os_old = machine.machine_type
            os_new = json_data['kernel']['uname_m']

            if os_old == '':
                machine.machine_type = os_new
                machine.save()
                os_old = os_new

            if machine.approved == False:
                error = 'The machine is not approved.'
                raise RuntimeError(error)

            elif os_old != os_new:
                error = 'Machine OS cannot change'
                raise RuntimeError(error)

        except Machine.DoesNotExist:
            error = "The machine is unavailable"
            raise RuntimeError(error)

        with transaction.atomic():

            os_version, kernel_version = parse_os_kernel(json_data)
            compiler_result = parse_compiler(json_data)
            branch, commit = parse_git(json_data)
            hardware_info = parse_hardware(json_data)
            postgres_info = parse_postgres(json_data)

            if json_data['meta']['benchmark'] == 'pgbench':
                benchmark_type_id = 1
            elif json_data['meta']['benchmark'] == 'tpch':
                benchmark_type_id = 2
            else:
                return HttpResponse(status=406)

            if 'git_clone_log' not in json_data:
                git_clone_log = ''
            else:
                git_clone_log = json_data['git_clone_log']

            if 'build_log' not in json_data:
                build_log = ''
            else:
                build_log = json_data['build_log']

            if 'cleanup_log' not in json_data:
                cleanup_log = ''
            else:
                cleanup_log = json_data['cleanup_log']

            if 'configure_log' not in json_data:
                configure_log = ''
            else:
                configure_log = json_data['configure_log']

            if 'install_log' not in json_data:
                install_log = ''
            else:
                install_log = json_data['install_log']

            postgres_log = json_data['pg_ctl']
            benchmark_log = None
            if benchmark_type_id == 1:
                benchmark_log = json_data['pgbench_log']

                # before doing anything else related to benchmarks, save the run
            new_run_info = RunInfo(
                machine_id=machine,
                hardware_info=hardware_info,
                compiler=compiler_result,
                git_branch=branch,
                git_commit=commit,
                git_clone_log=git_clone_log,
                configure_log=configure_log,
                build_log=build_log,
                install_log=install_log,
                benchmark_log=benchmark_log,
                benchmark=BenchmarkType.objects.get(pk=benchmark_type_id),
                cleanup_log=cleanup_log,
                postgres_log=postgres_log,
                postgres_info=postgres_info,
                run_received_time=json_data['run_received_time'],
                run_start_time=json_data['run_start_time'],
                run_end_time=json_data['run_end_time'],
                git_pull_runtime=json_data['git_pull_runtime'],
                git_clone_runtime=json_data['git_clone_runtime'],
                configure_runtime=json_data['configure_runtime'],
                build_runtime=json_data['build_runtime'],
                install_runtime=json_data['install_runtime'],
                cleanup_runtime=json_data['cleanup_runtime'],
                os_version_id=os_version,
                os_kernel_version_id=kernel_version,
                sysctl_raw=json_data['sysctl_log']
            )

            try:
                new_run_info.save()

            except Exception as e:

                raise RuntimeError(e)

            # now continue with benchmarks
           
            
            if benchmark_type_id == 1:
                if(json_data.get("pgbench")==None ):
                    benchmark_type="pgbench_custom"
                    data_json=json_data["pgbench_custom"]
                else:
                    benchmark_type="pgbench"
                    data_json=json_data["pgbench"]


            
                for item in data_json:

                    for client in item['clients']:
                        pgbench = parse_pgbench_options(item, client)

                        try:
                            pgbench_info = PgBenchBenchmark.objects.filter(clients=client, scale=pgbench['scale'],
                                                                           duration=pgbench['duration'],
                                                                           read_only=pgbench['read_only']).get()

                        except PgBenchBenchmark.DoesNotExist:

                            pgbench_info = PgBenchBenchmark(clients=client, scale=pgbench['scale'],
                                                            duration=pgbench['duration'],
                                                            read_only=pgbench['read_only'])

                            try:

                                pgbench_info.save()

                            except Exception as e:
                                raise RuntimeError(e)

                for item in data_json:
                    parse_pgbench_results(item,benchmark_type, new_run_info, json_data['pgbench_log_aggregate'], machine.owner_id)

            elif benchmark_type_id == 2:
                try:
                    tpch_config = TpchConfig.objects.filter(scale_factor=json_data['scale_factor']).get()

                except TpchConfig.DoesNotExist:
                    tpch_config = TpchConfig(scale_factor=json_data['scale_factor'],
                                                streams=json_data['num_streams'])

                    try:
                        tpch_config.save()

                    except Exception as e:
                        raise RuntimeError(e)
                    

                parse_tpch_query_plans(json_data["query_plans"])
                parse_tpch_results(new_run_info, tpch_config, json_data['qphh_size'], json_data['power_size'], json_data['throughput_size'],
                                   json_data['power'], json_data['throughput'], machine.owner_id)
                parse_explain_results(json_data["explaine_results"],new_run_info, tpch_config, json_data['qphh_size'], json_data['power_size'], json_data['throughput_size'])
                parse_explain_results_costOff(json_data["explaine_results_costOff"],new_run_info, tpch_config, json_data['qphh_size'], json_data['power_size'], json_data['throughput_size'])

    except Exception as e:

        if error == '':
            error = e

        try:
            error_object = RunLog(machine=machine, logmessage=str(error))
            error_object.save()
            print(error)


        except Exception as e:

            with open(os.path.join(sys.path[0], "log.txt"), "a+") as f:
                error_string = str(datetime.now()) + ' ' + str(error)
                f.write(error_string)

        return HttpResponse(status=406)

    print('Upload successful!')
    return HttpResponse(status=201)
