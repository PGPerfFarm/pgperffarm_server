from django.urls import re_path

from machines import views

urlpatterns = [
    re_path('list', views.machines_view, name='machines'),
    re_path('user', views.my_machines_view),
    re_path('add', views.add_machine_view),
    re_path('approve', views.approve_machine_view),
    re_path(r'edit/(?P<id>.+)/', views.edit_machine_view),
]
