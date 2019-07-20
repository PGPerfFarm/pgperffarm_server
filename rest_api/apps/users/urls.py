from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from users import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet),
router.register(r'machine-records-by-branch', views.UserMachineRecordByBranchListViewSet, base_name="machine-records-by-branch")
 
urlpatterns = [
	url(r'^', include(router.urls))
]
