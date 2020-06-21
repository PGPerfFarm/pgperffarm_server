from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from machines import views

router = DefaultRouter()
router.register(r'machines', views.MachineViewSet)
router.register(r'my_machines', views.MyMachineViewSet, base_name="my_machines")
router.register(r'add_machine', views.AddMachineViewSet, base_name="add_machine")

 
urlpatterns = [
	url(r'^', include(router.urls))
]