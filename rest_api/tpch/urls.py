from django.conf.urls import url

from tpch import views

app_name = "tpch"

urlpatterns = [
    url('machines', views.index, name='index'),
    url('upload', views.create_tpch_run, name='upload'),
]