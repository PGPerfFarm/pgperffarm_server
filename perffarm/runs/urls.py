from django.urls import re_path

from runs import views

urlpatterns = [
    re_path('upload', views.create_run_info, name='upload'),
    re_path(r'(?P<id>.+)/', views.single_run_view, name='run'),
]
