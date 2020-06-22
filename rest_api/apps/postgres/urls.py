from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from postgres import views

router = DefaultRouter()
router.register(r'postgres_settings_sets', views.PostgresSettingsSetViewSet)

urlpatterns = [
	url(r'^', include(router.urls))
]