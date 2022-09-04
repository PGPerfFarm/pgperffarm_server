from django.conf.urls import url

from machines import views

app_name = "machines"

urlpatterns = [
    url('index', views.index, name='index'),
    url('list', views.machines_view, name='machines'),
    url('user', views.my_machines_view, name='usermachine'),
    url('add', views.add_machine_view, name='addMachine'),
    url('approve', views.approve_machine_view),
    url(r'edit/(?P<id>.+)/', views.edit_machine_view),
]
