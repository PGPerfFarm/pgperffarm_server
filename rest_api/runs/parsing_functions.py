import csv
import json
import hashlib
import io
import re
from datetime import datetime

from postgres.models import PostgresSettingsSet, PostgresSettings
from benchmarks.models import PgBenchBenchmark, PgBenchResult, PgBenchStatement, PgBenchLog, PgBenchRunStatement, PgBenchPgStatStatements
from systems.models import HardwareInfo, Compiler, Kernel, OsDistributor, OsKernelVersion, OsVersion
from runs.models import GitRepo, Branch


def parse_sysctl(raw_data):

    data = json.loads(raw_data)
    json_dict = {}

    known_sysctl_linux = Kernel.objects.filter(kernel_id=1).get()

    for parameter in known_sysctl_linux.sysctl:

        if parameter in data:
            json_dict.update({parameter: data[parameter]})

    known_sysctl_mac = Kernel.objects.filter(kernel_id=2).get()

    for parameter in known_sysctl_mac.sysctl:

        if parameter in data:
            json_dict.update({parameter: data[parameter]})

    if json_dict == {}:
        return 'known sysctl info not found'

    else:
        return json_dict


def hash(json_data):

    hash_value = hashlib.sha256(json.dumps(json_data).encode('utf-8'))
    return hash_value.hexdigest()


def parse_linux_data(json_data):

    if ('brand' in json_data['system']['cpu']['information']):
        brand = json_data['system']['cpu']['information']['brand']

    else:
        brand = json_data['system']['cpu']['information']['brand_raw']

    if ('hz_actual_raw' in json_data['system']['cpu']['information']):
        hz = json_data['system']['cpu']['information']['hz_actual_raw'][0]

    else:
        hz = json_data['system']['cpu']['information']['hz_actual'][0]

    sysctl = parse_sysctl(json_data['sysctl_log'])

    result = {
        'cpu_brand': brand,
        'hz': hz,
        'cpu_cores': json_data['system']['cpu']['information']['count'],
        'total_memory': json_data['system']['memory']['virtual']['total'],
        'total_swap': json_data['system']['memory']['swap']['total'],
        'mounts_hash': hash(json_data['system']['memory']['mounts']),
        'mounts': json_data['system']['memory']['mounts'],
        'sysctl': sysctl,
        'sysctl_hash': hash(sysctl)
    }

    return result


def get_hash(postgres_settings):

    reader = csv.DictReader(io.StringIO(postgres_settings))
    postgres_settings_json = json.loads(json.dumps(list(reader)))

    hash_json = []

    for setting in postgres_settings_json:
        if setting['source'] != "default" and setting['source'] != "client":
            hash_json.append(setting)

    hash_string = hash(hash_json)

    return hash_string, hash_json


def add_postgres_settings(hash_value, settings):

    settings_set = PostgresSettingsSet.objects.filter(settings_sha256=hash_value).get()

    # now parsing all settings
    for row in settings:
        name = row['name']
        unit = row['source']
        value = row['setting']

        postgres_settings = PostgresSettings(db_settings_id=settings_set, setting_name=name, setting_unit=unit, setting_value=value)

        try:
            postgres_settings.save()

        except Exception as e:
            raise RuntimeError(e)


def parse_pgbench_options(item, clients):

    result = {
        'clients': clients,
        'scale': item['scale'],
        'duration': item['duration'],
        'read_only': item['read_only']
    }

    return result


def parse_pgbench_statement_latencies(statement_latencies, pgbench_result_id):

    # extract the nonempty statements
    statements = statement_latencies.split("\n")
    statements = list(filter(None, statements))

    line_id = 0

    for statement in statements:
        latency = re.findall('\d+\.\d+', statement)[0]
        text = (statement.split(latency)[1]).strip()

        try:
            pgbench_statement = PgBenchStatement.objects.filter(statement=text).get()

        except PgBenchStatement.DoesNotExist:

            pgbench_statement = PgBenchStatement(statement=text)

            try:
                pgbench_statement.save()

            except Exception as e:
                raise RuntimeError(e)

        run_statement = PgBenchRunStatement(latency=latency, line_id=line_id, pgbench_result_id=pgbench_result_id, result_id=pgbench_statement)

        try:
            run_statement.save()
            line_id += 1

        except Exception as e:
            raise RuntimeError(e)


def parse_pgbench_log_values(result, values):

    lines = values.splitlines()

    for line in lines:
        results = line.split()

        date = datetime.utcfromtimestamp(int(results[0])).strftime("%Y-%m-%dT%H:%M:%S%z")

        log = PgBenchLog(pgbench_result_id=result, interval_start=date, num_transactions=results[1], sum_latency=results[2], sum_latency_2=results[3], min_latency=results[4], max_latency=results[5])

        try:
            log.save()

        except Exception as e:
            raise RuntimeError(e)


def parse_pgbench_logs(result, log_array, iteration):

    found = False

    for log in log_array:

        for key, value in log.items():

            # tag-scale-duration-clients-iteration
            configs = key.split('-')

            if configs[1] == 'ro':
                read_only = True
            else:
                read_only = False

            # first of all, check that the config of each benchmark actually exists
            pgbench_config = PgBenchBenchmark.objects.filter(clients=configs[4], scale=configs[2], duration=configs[3], read_only=read_only).get()

            # then, check if it is the same as the test result
            if pgbench_config.pgbench_benchmark_id == result.benchmark_config.pgbench_benchmark_id:
                if int(configs[5]) == iteration:
                    parse_pgbench_log_values(result, value)
                    found = True

    # if no match has been found, return error
    if not found:
        raise RuntimeError('Invalid PgBench logs.')


def parse_pg_stat_statements(pgbench_result_id, result):
    for item in result:
        query = item['query']
        total_exec_time = item['total_exec_time']
        min_exec_time = item['min_exec_time']
        max_exec_time = item['max_exec_time']
        mean_exec_time = item['mean_exec_time']
        stddev_exec_time = item['stddev_exec_time']
        rows = item['rows']

        pg_stat_statements = PgBenchPgStatStatements(pgbench_result_id=pgbench_result_id, query=query, total_exec_time=total_exec_time, min_exec_time=min_exec_time, max_exec_time=max_exec_time, mean_exec_time=mean_exec_time, stddev_exec_time=stddev_exec_time, rows=rows)

        try:
            pg_stat_statements.save()

        except Exception as e:
            raise RuntimeError(e)


def parse_pgbench_results(item, run_id, pgbench_log):

    json = item['iterations']
    iterations = 0

    for client in item['clients']:

        for result in json:

            if int(result['clients']) == client:

                pgbench_config = PgBenchBenchmark.objects.filter(clients=result['clients'], scale=item['scale'], duration=item['duration'], read_only=item['read_only']).get()

                pgbench_result_last = PgBenchResult.objects.order_by('-pgbench_result_id').first()

                if pgbench_result_last is None:
                    iterations = 0

                # assuming results get added in order
                elif (pgbench_result_last.benchmark_config.pgbench_benchmark_id == pgbench_config.pgbench_benchmark_id) and (pgbench_result_last.run_id.run_id == run_id):
                    iterations += 1

                else:
                    iterations = 0

                # remove statement latencies
                statement_latencies = result['statement_latencies']

                result_object = PgBenchResult(run_id=run_id, benchmark_config=pgbench_config, tps=result['tps'], mode=result['mode'], latency=result['latency'], start=result['start'], end=result['end'], iteration=result['iteration'], init=result['init'])

                try:
                    result_object.save()

                    parse_pgbench_logs(result_object, pgbench_log, iterations)
                    parse_pgbench_statement_latencies(statement_latencies, result_object)

                    # parse pg_stat_statements
                    pg_stat_statements = result['pg_stat_statements']
                    parse_pg_stat_statements(result_object, pg_stat_statements)

                except Exception as e:
                    raise RuntimeError(e)


def parse_os_kernel(json_data):
    try:
        os_distributor = OsDistributor.objects.filter(dist_name=json_data['os_information']['distributor']).get()

    except OsDistributor.DoesNotExist:

        try:

            os_distributor = OsDistributor(dist_name=json_data['os_information']['distributor'])
            os_distributor.save()

        except Exception as e:
            raise RuntimeError(e)
    try:
        os_kernel = Kernel.objects.filter(kernel_name=json_data['kernel']['uname_s']).get()

    except Kernel.DoesNotExist:

        try:

            os_kernel = Kernel(kernel_name=json_data['kernel']['uname_s'])
            os_kernel.save()

        except Exception as e:
            raise RuntimeError(e)

    try:
        os_version = OsVersion.objects.filter(dist_id=os_distributor.os_distributor_id, release=json_data['os_information']['release'], codename=json_data['os_information']['codename'], description=json_data['os_information']['description']).get()

    except OsVersion.DoesNotExist:

        try:

            os_version = OsVersion(dist_id=os_distributor, release=json_data['os_information']['release'], codename=json_data['os_information']['codename'], description=json_data['os_information']['description'])
            os_version.save()

        except Exception as e:
            raise RuntimeError(e)

    try:
        kernel_version = OsKernelVersion.objects.filter(kernel_id=os_kernel.kernel_id, kernel_release=json_data['kernel']['uname_r'], kernel_version=json_data['kernel']['uname_v']).get()

    except OsKernelVersion.DoesNotExist:

        try:

            kernel_version = OsKernelVersion(kernel_id=os_kernel, kernel_release=json_data['kernel']['uname_r'], kernel_version=json_data['kernel']['uname_v'])
            kernel_version.save()

        except Exception as e:
            raise RuntimeError(e)

    return os_version, kernel_version


def parse_compiler(json_data):
    compiler_raw = json_data['compiler']
    compiler_match = re.search('compiled by (.*),', compiler_raw)

    if compiler_match:
        compiler = compiler_match.group(1)

    else:
        compiler = 'impossible to parse compiler'

    try:
        compiler_result = Compiler.objects.filter(compiler=compiler).get()

    except Compiler.DoesNotExist:

        try:

            compiler_result = Compiler(compiler=compiler)
            compiler_result.save()

        except Exception as e:
            raise RuntimeError(e)

    return compiler_result


def parse_git(json_data):
    try:
        repo = GitRepo.objects.filter(url=json_data['git']['remote']).get()

    except GitRepo.DoesNotExist:

        try:

            repo = GitRepo(url=json_data['git']['remote'])
            repo.save()

        except Exception as e:
            raise RuntimeError(e)

    try:
        branch = Branch.objects.filter(name=json_data['git']['branch'], git_repo=repo.git_repo_id).get()

    except Branch.DoesNotExist:

        try:

            branch = Branch(name=json_data['git']['branch'], git_repo=repo)
            branch.save()

        except Exception as e:
            raise RuntimeError(e)

    commit = json_data['git']['commit']

    return branch, commit


def parse_hardware(json_data):
    hardware_info_new = parse_linux_data(json_data)

    try:
        hardware_info = HardwareInfo.objects.filter(cpu_brand=hardware_info_new['cpu_brand'], cpu_cores=hardware_info_new['cpu_cores'], hz=hardware_info_new['hz'], total_memory=hardware_info_new['total_memory'], total_swap=hardware_info_new['total_swap'], sysctl_hash=hardware_info_new['sysctl_hash'], mounts_hash=hardware_info_new['mounts_hash']).get()

    except HardwareInfo.DoesNotExist:

        try:

            hardware_info = HardwareInfo(cpu_brand=hardware_info_new['cpu_brand'], cpu_cores=hardware_info_new['cpu_cores'], hz=hardware_info_new['hz'], total_memory=hardware_info_new['total_memory'], total_swap=hardware_info_new['total_swap'], sysctl_hash=hardware_info_new['sysctl_hash'], mounts_hash=hardware_info_new['mounts_hash'], sysctl=hardware_info_new['sysctl'], mounts=hardware_info_new['mounts'])

            hardware_info.save()

        except Exception as e:
            raise RuntimeError(e)

    return hardware_info


def parse_postgres(json_data):
    postgres_hash, postgres_hash_object = get_hash(json_data['postgres_settings'])

    try:
        postgres_info = PostgresSettingsSet.objects.filter(settings_sha256=postgres_hash).get()

    except PostgresSettingsSet.DoesNotExist:

        try:

            postgres_info = PostgresSettingsSet(settings_sha256=postgres_hash)
            postgres_info.save()
            add_postgres_settings(postgres_hash, postgres_hash_object)

        except Exception as e:
            raise RuntimeError(e)

    return postgres_info


def parse_collectd(json_data):

    def parse_collectd_key(collectd_key):
        date = re.search('-\d\d\d\d-\d\d-\d\d', collectd_key).group(0)
        collectd_key = collectd_key.replace(date, '')
        return collectd_key

    collectd = list(json_data['collectd'].values())[0]

    cpu_average = collectd['aggregation-cpu-average']
    processes = collectd['processes']
    contextswitch = collectd['contextswitch']
    ipc_shm = collectd['ipc-shm']
    ipc_msg = collectd['ipc-msg']
    ipc_sem = collectd['ipc-sem']
    memory = collectd['memory']
    swap = collectd['swap']
    vmem = collectd['vmem']
    postgres = collectd['postgresql-postgres']
