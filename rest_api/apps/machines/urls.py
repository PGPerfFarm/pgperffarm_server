from django.conf.urls import url
from machines import views

urlpatterns = [
	url('machines/', views.machine_list),
	url('machines/<int:sn>/', views.machine_detail),
]