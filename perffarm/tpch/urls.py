from django.conf.urls import url

from tpch import views
from django.urls import path
app_name = "tpch"
from .views import explain_results,explain_results_CostOn

urlpatterns = [
    url('machines', views.index, name='index'),
    url(r'details/(?P<id>.+)/', views.details, name='details'),
    url(r'trends/(?P<machine>.+)/(?P<scale>.+)/', views.trend, name='tpch_trend'),
    url(r'runs_commit/(?P<machine>.+)/(?P<scale>.+)/(?P<commit>.+)/', views.runs_commit_view, name='runs_commit'),

    url(r'explain-results_costOff/(?P<id>.+)/', explain_results, name='explain_results'),
    url(r'explain_results_CostOn/(?P<id>.+)/', explain_results_CostOn, name='explain_results_CostOn'),
    
]