from django.conf.urls import url

from machines import views

urlpatterns = [
    url('machine_user', views.MyMachinesView),
    url('machines', views.MachinesView, name="machines"),
    url(r'edit_machine/(?P<id>.+)/', views.EditMachineView),
    url('add_machine', views.AddMachineView),
]
