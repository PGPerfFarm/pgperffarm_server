from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from runs import views

router = DefaultRouter()
router.register(r'runs', views.RunViewSet)
router.register(r'branches', views.BranchViewSet)

urlpatterns = [
	url(r'^', include(router.urls)),
	url(r'upload/$', views.CreateRunInfo, name="upload")
]