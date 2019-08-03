from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from users import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, base_name="users"),
router.register(r'machine-records-by-branch', views.UserMachineRecordByBranchListViewSet, base_name="machine-records-by-branch")
 
# https://django-rest-auth.readthedocs.io/en/latest/api_endpoints.html
urlpatterns = [
	url(r'^', include(router.urls)),
	url(r'^rest-auth/', include('rest_auth.urls')),
	url(r'^', include('django.contrib.auth.urls')),
	# url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
	url(r'^rest-auth/facebook/$', views.FacebookLogin.as_view(), name='fb_login'),
	url(r'^rest-auth/twitter/$', views.TwitterLogin.as_view(), name='twitter_login'),
	url(r'^rest-auth/github/$', views.GithubLogin.as_view(), name='github_login'),
	url(r'^rest-auth/google/$', views.GoogleLogin.as_view(), name='google_login'),
	url(r'^rest-auth/microsoft/$', views.MicrosoftLogin.as_view(), name='microsoft_login'),
]
