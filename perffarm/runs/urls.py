from django.conf.urls import url

from runs import views

urlpatterns = [
    url('upload', views.create_run_info, name='upload'),
    url(r'(?P<id>.+)/', views.single_run_view, name='run'),
]
