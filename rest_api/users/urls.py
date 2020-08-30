from django.conf.urls import include, url
from users import auth

urlpatterns = [
	url(r'^(?:accounts/)?community_login/?$', auth.login, name='community_login'),
	url(r'^(?:accounts/)?logout/?$', auth.logout),
	url(r'^auth_receive/$', auth.auth_receive),
]

