from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from machines import views

router = DefaultRouter()
router.register(r'machines', views.MachineViewSet)
router.register(r'machine-records', views.MachineHistoryRecordViewSet, base_name="machine-records")
 
urlpatterns = [
	url(r'^', include(router.urls))
]