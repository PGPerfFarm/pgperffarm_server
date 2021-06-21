from django.conf.urls import url

from machines import views

urlpatterns = [
    url('machine_user', views.my_machines_view),
    url('machines', views.machines_view, name="machines"),
    url(r'edit_machine/(?P<id>.+)/', views.edit_machine_view),
    url('add_machine', views.add_machine_view),
    url('approve_machine', views.approve_machine_view),
]
