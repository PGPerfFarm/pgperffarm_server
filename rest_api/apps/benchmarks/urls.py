from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from benchmarks import views

router = DefaultRouter()
router.register(r'benchmarks', views.PgBenchBenchmarkViewSet)
router.register(r'pgbench_results', views.PgBenchResultViewSet)
router.register(r'pgbench_statements', views.PgBenchStatementViewSet)
router.register(r'pgbench_run_statements', views.PgBenchRunStatementViewSet)
router.register(r'benchmarks_machines', views.PgBenchBenchmarkMachinesViewSet)


urlpatterns = [
	url(r'^', include(router.urls))
]