from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from systems import views

router = DefaultRouter()
router.register(r'systems', views.SystemViewSet)
 
urlpatterns = [
	url(r'^', include(router.urls)),
]