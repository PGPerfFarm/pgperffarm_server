from django.conf.urls import url

from tpch import views

app_name = "tpch"

urlpatterns = [
    url('machines', views.index, name='index'),
    url('upload', views.create_tpch_run, name='upload'),
    url(r'details/(?P<id>.+)/', views.details, name='details'),
    url(r'trends/(?P<machine>.+)/(?P<scale>.+)/', views.trend, name='tpch_trend'),
]