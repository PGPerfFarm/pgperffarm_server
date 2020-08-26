from benchmarks.models import PgBenchBenchmark, PgBenchResult, PgBenchStatement, PgBenchRunStatement
from benchmarks.serializers import PgBenchResultSerializer, PgBenchBenchmarkSerializer, PgBenchRunStatementSerializer, PgBenchStatementSerializer, PgBenchConfigMachineSerializer, PgBenchResultCompleteSerializer, PgBenchTrendSerializer, PgBenchRunsSerializer, MachineHistorySerializer, PostgresHistorySerializer, OverviewSerializer
from runs.models import RunInfo
from machines.models import Machine

from rest_framework import permissions, renderers, viewsets, mixins, authentication, serializers, status, pagination, generics


class TrendPagination(pagination.PageNumberPagination):       
       page_size = 200


class PgBenchBenchmarkViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	queryset =  PgBenchBenchmark.objects.all().order_by('pgbench_benchmark_id')
	serializer_class = PgBenchBenchmarkSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )
	pagination_class = TrendPagination


class PgBenchResultCompleteViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	queryset =  PgBenchResult.objects.all().order_by('-pgbench_result_id')
	serializer_class = PgBenchResultCompleteSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )
	pagination_class = TrendPagination


class PostgresHistoryViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	serializer_class = PostgresHistorySerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )
	pagination_class = TrendPagination

	def get_queryset(self):

		machine = int(self.kwargs['machine'])


		queryset = Machine.objects.raw("with a as (select p1.machine_id_id, p1.name, p1.db_settings_id_id settings1, p2.db_settings_id_id settings2, p1.setting_name, p1.setting_value value1, p1.setting_unit unit1, p2.setting_value value2, p2.setting_unit unit2 from (select * from postgres_postgressettings, runs_runinfo, runs_branch, machines_machine where postgres_postgressettings.db_settings_id_id = runs_runinfo.postgres_info_id and runs_branch.branch_id = runs_runinfo.git_branch_id and machines_machine.machine_id = runs_runinfo.machine_id_id and machine_id_id = %s) p1, (select * from postgres_postgressettings, runs_runinfo, runs_branch, machines_machine where postgres_postgressettings.db_settings_id_id = runs_runinfo.postgres_info_id and runs_branch.branch_id = runs_runinfo.git_branch_id and machines_machine.machine_id = runs_runinfo.machine_id_id and machine_id_id = %s) p2 where p1.db_settings_id_id < p2.db_settings_id_id and p1.setting_name = p2.setting_name and p1.name = p2.name and (p1.setting_value <> p2.setting_value or p1.setting_unit <> p2.setting_unit)), b as (select machine_id, alias, machine_type, kernel_name, name, min(run_id), min(runs_runinfo.add_time) add_time, postgres_info_id from machines_machine, runs_runinfo, runs_branch, systems_oskernelversion, systems_kernel where runs_runinfo.machine_id_id = machines_machine.machine_id and runs_runinfo.git_branch_id = runs_branch.branch_id and runs_runinfo.os_kernel_version_id_id = systems_oskernelversion.os_kernel_version_id and systems_oskernelversion.kernel_id_id = systems_kernel.kernel_id and machine_id = %s group by name, postgres_info_id, machine_id, alias, machine_type, kernel_name order by name, min), c as (select postgres_info_id prev, lead(postgres_info_id) over(partition by name) as next from b) select distinct min, add_time, settings1, settings2, setting_name, unit1, unit2, value1, value2, b.machine_id, a.name, machine_type, alias, kernel_name, first_run, last_run, min_add_time, max_add_time from a, b, c, (select max(run_id) last_run, max(add_time) max_add_time from runs_runinfo where machine_id_id = %s) d, (select min(run_id) first_run, min(add_time) min_add_time from runs_runinfo where machine_id_id = %s) e where a.settings1 = c.prev and a.settings2 = c.next and a.settings2 = b.postgres_info_id order by min;", [machine, machine, machine, machine, machine])

		return queryset


class OverviewViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	queryset = PgBenchBenchmark.objects.raw("select * from (select max(run_id) last_run, max(runs_runinfo.add_time) last_run_time, count(distinct run_id) runs, count(distinct dist_name) os_count, count(distinct pgbench_result_id) results_count, count(distinct benchmark_config_id) configs, count(distinct name) branches, count(distinct git_repo_id) repos from runs_runinfo, runs_branch, systems_osversion, systems_osdistributor, benchmarks_pgbenchresult where runs_runinfo.git_branch_id = runs_branch.branch_id and runs_runinfo.os_version_id_id = systems_osversion.os_version_id and systems_osversion.dist_id_id = systems_osdistributor.os_distributor_id and benchmarks_pgbenchresult.run_id_id = runs_runinfo.run_id) t1, (select count(distinct machine_id) machines_count, count(distinct owner_id_id) users from machines_machine) t2, (select count(run_id) recent_runs from runs_runinfo where add_time > 'now'::timestamp - '1 month'::interval) t3, (select machine_id_id last_machine_id, alias last_machine_alias from machines_machine, runs_runinfo where runs_runinfo.machine_id_id = machines_machine.machine_id and run_id = (select max(run_id) from runs_runinfo)) t4, (select * from (select machine_id_id, pgbench_benchmark_id, count(pgbench_result_id), scale, clients, duration, read_only from runs_runinfo, benchmarks_pgbenchresult, benchmarks_pgbenchbenchmark where runs_runinfo.run_id = benchmarks_pgbenchresult.run_id_id and benchmarks_pgbenchresult.benchmark_config_id = benchmarks_pgbenchbenchmark.pgbench_benchmark_id group by machine_id_id, pgbench_benchmark_id, scale, clients, duration, read_only) tmp where count = (select max(count) from (select machine_id_id, pgbench_benchmark_id, count(pgbench_result_id), scale, clients, duration, read_only from runs_runinfo, benchmarks_pgbenchresult, benchmarks_pgbenchbenchmark where runs_runinfo.run_id = benchmarks_pgbenchresult.run_id_id and benchmarks_pgbenchresult.benchmark_config_id = benchmarks_pgbenchbenchmark.pgbench_benchmark_id group by machine_id_id, pgbench_benchmark_id, scale, clients, duration, read_only) tmp) limit 1) t5;")

	serializer_class = OverviewSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )
	pagination_class = TrendPagination


class PgBenchBenchmarkMachinesViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	queryset = PgBenchBenchmark.objects.raw("select pgbench_benchmark_id, scale, duration, read_only, clients, machine_id, alias, machines_machine.description, machines_machine.add_time, machine_type, username, count(pgbench_benchmark_id) from benchmarks_pgbenchbenchmark, benchmarks_pgbenchresult, runs_runinfo, machines_machine, auth_user where benchmarks_pgbenchbenchmark.pgbench_benchmark_id = benchmarks_pgbenchresult.benchmark_config_id and benchmarks_pgbenchresult.run_id_id = runs_runinfo.run_id and runs_runinfo.machine_id_id = machines_machine.machine_id and machines_machine.owner_id_id = auth_user.id group by machine_id, alias, machines_machine.description, machines_machine.add_time, machine_type, username, pgbench_benchmark_id, scale, duration, read_only, clients;")

	serializer_class = PgBenchConfigMachineSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )
	pagination_class = TrendPagination


class MachineHistoryViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	serializer_class = MachineHistorySerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )
	pagination_class = TrendPagination

	def get_queryset(self):

		machine = int(self.kwargs['machine'])

		queryset = Machine.objects.raw("select machine_id, alias, machines_machine.description, machines_machine.add_time, machine_type, username, email, url, dist_name, kernel_name, kernel_release, kernel_version, release, codename, compiler, name, url, min(run_id) as run_id, count(run_id), postgres_info_id, mounts, systems_hardwareinfo.sysctl, runs_runinfo.hardware_info_id, pgbench_benchmark_id, scale, duration, read_only, clients from runs_gitrepo, benchmarks_pgbenchbenchmark, benchmarks_pgbenchresult, runs_runinfo, runs_branch, machines_machine, auth_user, systems_compiler, systems_oskernelversion, systems_kernel, systems_osdistributor, systems_osversion, systems_hardwareinfo where benchmarks_pgbenchbenchmark.pgbench_benchmark_id = benchmarks_pgbenchresult.benchmark_config_id and runs_branch.git_repo_id = runs_gitrepo.git_repo_id and benchmarks_pgbenchresult.run_id_id = runs_runinfo.run_id and runs_runinfo.git_branch_id = runs_branch.branch_id and systems_hardwareinfo.hardware_info_id = runs_runinfo.hardware_info_id and runs_runinfo.machine_id_id = machines_machine.machine_id and runs_runinfo.compiler_id = systems_compiler.compiler_id and machines_machine.owner_id_id = auth_user.id and runs_runinfo.os_version_id_id = systems_osversion.os_version_id and runs_runinfo.os_kernel_version_id_id = systems_oskernelversion.os_kernel_version_id and systems_oskernelversion.kernel_id_id = systems_kernel.kernel_id and systems_osversion.dist_id_id = systems_osdistributor.os_distributor_id and machine_id_id = %s group by url, dist_name, machines_machine.add_time, kernel_name, kernel_release, kernel_version, release, codename, mounts, systems_hardwareinfo.sysctl, compiler, name, postgres_info_id, runs_runinfo.hardware_info_id, pgbench_benchmark_id, scale, duration, read_only, clients, machine_id, alias, machines_machine.description, machine_type, username, email order by run_id desc;", [machine])

		return queryset


class PgBenchRunsViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	serializer_class = PgBenchRunsSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )
	pagination_class = TrendPagination

	def get_queryset(self):

		machine = int(self.kwargs['machine'])
		config = int(self.kwargs['config'])
		commit = '%' + str(self.kwargs['commit'])
 
		queryset = RunInfo.objects.raw("select runs_runinfo.run_id, pgbench_result_id, runs_runinfo.add_time from benchmarks_pgbenchbenchmark, benchmarks_pgbenchresult, runs_runinfo, runs_branch where runs_runinfo.git_branch_id = runs_branch.branch_id and benchmarks_pgbenchbenchmark.pgbench_benchmark_id = benchmarks_pgbenchresult.benchmark_config_id and benchmarks_pgbenchresult.run_id_id = runs_runinfo.run_id and git_commit like %s and machine_id_id = %s and benchmark_config_id = %s and runs_branch.git_repo_id < 5 order by add_time;", [commit, machine, config])

		return queryset


class PgBenchBenchmarkTrendViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	serializer_class = PgBenchTrendSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )
	pagination_class = TrendPagination

	def get_queryset(self):
		
		machine = int(self.kwargs['machine'])
		config = int(self.kwargs['config'])

		queryset = PgBenchBenchmark.objects.raw("select avg(tps) as avgtps, avg(latency) as avglat, stddev(tps) as stdtps, stddev(latency) as stdlat, min(tps) as mintps, min(latency) as minlat, max(tps) as maxtps, max(latency) as maxlat, min(runs_runinfo.add_time) as add_time, count(git_commit), git_commit, pgbench_benchmark_id, name, scale, duration, read_only, clients, machine_id, alias, machines_machine.description, machine_type, username, email, url, min(dist_name) as dist_name, min(kernel_name) as kernel_name, max(systems_compiler.compiler) as compiler from benchmarks_pgbenchbenchmark, benchmarks_pgbenchresult, runs_gitrepo, runs_runinfo, runs_branch, machines_machine, auth_user, systems_compiler, systems_oskernelversion, systems_kernel, systems_osdistributor, systems_osversion where benchmarks_pgbenchbenchmark.pgbench_benchmark_id = benchmarks_pgbenchresult.benchmark_config_id and runs_branch.git_repo_id = runs_gitrepo.git_repo_id and benchmarks_pgbenchresult.run_id_id = runs_runinfo.run_id and runs_runinfo.git_branch_id = runs_branch.branch_id and runs_runinfo.machine_id_id = machines_machine.machine_id and runs_runinfo.compiler_id = systems_compiler.compiler_id and machines_machine.owner_id_id = auth_user.id and runs_runinfo.os_version_id_id = systems_osversion.os_version_id and runs_runinfo.os_kernel_version_id_id = systems_oskernelversion.os_kernel_version_id and systems_oskernelversion.kernel_id_id = systems_kernel.kernel_id and systems_osversion.dist_id_id = systems_osdistributor.os_distributor_id and machine_id_id = %s and benchmark_config_id = %s and runs_branch.git_repo_id < 5 group by git_commit, name, pgbench_benchmark_id, url, machine_id, alias, machines_machine.description, machine_type, username, email,scale, duration, read_only, clients order by add_time desc;", [machine, config])

		return queryset


class PgBenchResultViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	queryset =  PgBenchResult.objects.all().order_by('pgbench_result_id')
	serializer_class = PgBenchResultSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )
	pagination_class = TrendPagination


class PgBenchStatementViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	queryset =  PgBenchStatement.objects.all().order_by('pgbench_statement_id')
	serializer_class = PgBenchStatementSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )
	pagination_class = TrendPagination


class PgBenchRunStatementViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	queryset =  PgBenchRunStatement.objects.all().order_by('pgbench_run_statement_id')
	serializer_class = PgBenchRunStatementSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )
	pagination_class = TrendPagination