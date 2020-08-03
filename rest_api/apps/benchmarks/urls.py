from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from benchmarks import views

router = DefaultRouter()
router.register(r'benchmarks', views.PgBenchBenchmarkViewSet)
router.register(r'pgbench_results', views.PgBenchResultViewSet)
router.register(r'pgbench_statements', views.PgBenchStatementViewSet)
router.register(r'pgbench_run_statements', views.PgBenchRunStatementViewSet)
router.register(r'benchmarks_machines', views.PgBenchBenchmarkMachinesViewSet)
router.register(r'pgbench_results_complete', views.PgBenchResultCompleteViewSet)
router.register(r'pgbench_trends/(?P<machine>.+)/(?P<config>.+)', views.PgBenchBenchmarkTrendViewSet, basename="pgbench_trends-detail")
router.register(r'pgbench_results_commit/(?P<commit>.+)/(?P<machine>.+)/(?P<config>.+)', views.PgBenchRunsViewSet, basename="pgbench_trends-commit")


urlpatterns = [
	url(r'^', include(router.urls))
]