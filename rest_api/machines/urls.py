from django.conf.urls import url

from machines import views

urlpatterns = [
    url('list', views.machines_view, name='machines'),
    url('user', views.my_machines_view),
    url('add', views.add_machine_view),
    url('approve', views.approve_machine_view),
    url(r'edit/(?P<id>.+)/', views.edit_machine_view),
]
