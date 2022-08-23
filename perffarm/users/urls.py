from django.urls import path, re_path

from users import auth

urlpatterns = [
    re_path('community_login', auth.login, name='community_login'),
    re_path('logout', auth.logout),
    path('auth_receive/', auth.auth_receive),
]
