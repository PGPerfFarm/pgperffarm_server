from django.urls import re_path

from benchmarks import views

urlpatterns = [
    re_path('overview', views.overview_view),
    re_path('machines', views.pgbench_benchmark_machines_view, name='benchmarks_machines'),
    re_path(r'history/(?P<machine>.+)/', views.machine_history_view),
    re_path(r'postgres/(?P<machine>.+)/', views.postgres_history_view, name='postgres-history'),
    re_path(r'pgbench_trends/(?P<machine>.+)/(?P<config>.+)/', views.pgbench_benchmark_trend_view, name='pgbench_trends-detail'),
    re_path(r'pgbench_results_commit/(?P<commit>.+)/(?P<machine>.+)/(?P<config>.+)/', views.pgbench_runs_view, name='pgbench_trends-commit'),
    re_path(r'pgbench_results_complete/(?P<id>.+)/', views.pgbench_result_complete_view),
]
