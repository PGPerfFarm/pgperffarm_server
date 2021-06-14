from django.conf.urls import url

from runs import views

urlpatterns = [
    url(r'upload/$', views.create_run_info, name="upload"),
    url(r'run/(?P<id>.+)/', views.single_run_view, name="run"),
]
