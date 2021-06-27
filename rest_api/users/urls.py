from django.conf.urls import url

from users import auth

urlpatterns = [
    url('community_login', auth.login, name='community_login'),
    url('logout', auth.logout),
    url(r'auth_receive/$', auth.auth_receive),
]
