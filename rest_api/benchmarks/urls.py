from django.conf.urls import include, url
from benchmarks import views
 
urlpatterns = [
	url('benchmarks', views.PgBenchBenchmarkView),
	url('pgbench_results_complete', views.PgBenchResultCompleteView),
	url(r'history/(?P<machine>.+)/', views.MachineHistoryView),
	url('overview', views.OverviewView),
	url(r'postgres/(?P<machine>.+)/', views.PostgresHistoryView, name="postgres-history"),
	url('benchmarks_machines', views.PgBenchBenchmarkMachinesView),
	url(r'pgbench_trends/(?P<machine>.+)/(?P<config>.+)/', views.PgBenchBenchmarkTrendView, name="pgbench_trends-detail"),
	url(r'pgbench_results_commit/(?P<commit>.+)/(?P<machine>.+)/(?P<config>.+)/', views.PgBenchRunsView, name="pgbench_trends-commit"),
]