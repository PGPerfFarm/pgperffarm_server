from django.conf.urls import url

from benchmarks import views

app_name = "benchmarks"

urlpatterns = [
    url('overview', views.overview_view),
    url(r'^machines/(?P<type>\w+)/$', views.pgbench_benchmark_machines_view, name='benchmarks_machines'),
    url(r'history/(?P<machine>.+)/', views.machine_history_view, name='machine_history'),
    url(r'postgres/(?P<machine>.+)/', views.postgres_history_view, name='postgres-history'),
    url(r'pgbench_trends/(?P<type>\w+)/(?P<machine>.+)/(?P<config>.+)/', views.pgbench_benchmark_trend_view, name='pgbench_trends-detail'),
    url(r'pgbench_results_commit/(?P<type>\w+)/(?P<commit>.+)/(?P<machine>.+)/(?P<config>.+)/', views.pgbench_runs_view, name='pgbench_trends-commit'),
    url(r'pgbench_results_complete/(?P<id>.+)/', views.pgbench_result_complete_view),
]
