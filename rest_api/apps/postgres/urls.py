from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from postgres import views

router = DefaultRouter()
router.register(r'postgres_settings_sets', views.PostgresSettingsSetViewSet)
router.register(r'postgres_settings', views.PostgresSettingsViewSet)

urlpatterns = [
	url(r'^', include(router.urls))
]