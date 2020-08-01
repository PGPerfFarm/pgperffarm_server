from benchmarks.models import PgBenchBenchmark, PgBenchResult, PgBenchStatement, PgBenchRunStatement
from benchmarks.serializers import PgBenchResultSerializer, PgBenchBenchmarkSerializer, PgBenchRunStatementSerializer, PgBenchStatementSerializer, PgBenchConfigMachineSerializer, PgBenchResultCompleteSerializer, PgBenchTrendSerializer

from rest_framework import permissions, renderers, viewsets, mixins, authentication, serializers, status, pagination, generics


class TrendPagination(pagination.PageNumberPagination):       
       page_size = 200


class PgBenchBenchmarkViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	queryset =  PgBenchBenchmark.objects.all().order_by('pgbench_benchmark_id')
	serializer_class = PgBenchBenchmarkSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )


class PgBenchResultCompleteViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	queryset =  PgBenchResult.objects.all().order_by('-pgbench_result_id')
	serializer_class = PgBenchResultCompleteSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )


class PgBenchBenchmarkMachinesViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	queryset = PgBenchBenchmark.objects.raw("select pgbench_benchmark_id, scale, duration, read_only, clients, machine_id, alias, machines_machine.add_time, machine_type, username, count(pgbench_benchmark_id) from benchmarks_pgbenchbenchmark, benchmarks_pgbenchresult, runs_runinfo, machines_machine, auth_user where benchmarks_pgbenchbenchmark.pgbench_benchmark_id = benchmarks_pgbenchresult.benchmark_config_id and benchmarks_pgbenchresult.run_id_id = runs_runinfo.run_id and runs_runinfo.machine_id_id = machines_machine.machine_id and machines_machine.owner_id_id = auth_user.id group by machine_id, alias, machines_machine.add_time, machine_type, username, pgbench_benchmark_id, scale, duration, read_only, clients;")

	serializer_class = PgBenchConfigMachineSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )


class PgBenchBenchmarkTrendViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	serializer_class = PgBenchTrendSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )
	pagination_class = TrendPagination

	def get_queryset(self):
		
		machine = int(self.kwargs['machine'])
		config = int(self.kwargs['config'])

		queryset = PgBenchBenchmark.objects.raw("select avg(tps) as avgtps, avg(latency) as avglat, stddev(tps) as stdtps, stddev(latency) as stdlat, min(runs_runinfo.add_time) as add_time, count(git_commit), git_commit, pgbench_benchmark_id, name, scale, duration, read_only, clients, machine_id, alias, machine_type, username, email, url, min(dist_name) as dist_name, min(kernel_name) as kernel_name, max(systems_compiler.compiler) as compiler from benchmarks_pgbenchbenchmark, benchmarks_pgbenchresult, runs_gitrepo, runs_runinfo, runs_branch, machines_machine, auth_user, systems_compiler, systems_oskernelversion, systems_kernel, systems_osdistributor, systems_osversion where benchmarks_pgbenchbenchmark.pgbench_benchmark_id = benchmarks_pgbenchresult.benchmark_config_id and runs_runinfo.git_repo_id = runs_gitrepo.git_repo_id and benchmarks_pgbenchresult.run_id_id = runs_runinfo.run_id and runs_runinfo.git_branch_id = runs_branch.branch_id and runs_runinfo.machine_id_id = machines_machine.machine_id and runs_runinfo.compiler_id = systems_compiler.compiler_id and machines_machine.owner_id_id = auth_user.id and runs_runinfo.os_version_id_id = systems_osversion.os_version_id and runs_runinfo.os_kernel_version_id_id = systems_oskernelversion.os_kernel_version_id and systems_oskernelversion.kernel_id_id = systems_kernel.kernel_id and systems_osversion.dist_id_id = systems_osdistributor.os_distributor_id and machine_id_id = %s and benchmark_config_id = %s and runs_runinfo.git_repo_id = 9 group by git_commit, name, pgbench_benchmark_id, url, machine_id, alias, machine_type, username, email,scale, duration, read_only, clients order by add_time desc;", [machine, config])

		return queryset


class PgBenchResultViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	queryset =  PgBenchResult.objects.all().order_by('pgbench_result_id')
	serializer_class = PgBenchResultSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )


class PgBenchStatementViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	queryset =  PgBenchStatement.objects.all().order_by('pgbench_statement_id')
	serializer_class = PgBenchStatementSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )


class PgBenchRunStatementViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	queryset =  PgBenchRunStatement.objects.all().order_by('pgbench_run_statement_id')
	serializer_class = PgBenchRunStatementSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )