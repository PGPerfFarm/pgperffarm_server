from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from users import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
 
# https://django-rest-auth.readthedocs.io/en/latest/api_endpoints.html
urlpatterns = [
	url(r'^', include(router.urls)),
	url(r'^', include('django.contrib.auth.urls')),
	#url('login', auth.login),
	#url('logout', auth.logout),
	#url('auth_receive', auth.auth_receive)
]
