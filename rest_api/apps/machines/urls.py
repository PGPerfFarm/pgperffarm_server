from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from machines import views

router = DefaultRouter()
router.register(r'machines', views.MachineViewSet)
router.register(r'my-machines', views.UserMachineViewSet, base_name="my-machines")
router.register(r'aliases', views.AliasViewSet, base_name="aliases")
 
urlpatterns = [
	url(r'^', include(router.urls))
]