from django.conf.urls import url

from runs import views

urlpatterns = [
    url(r'upload/$', views.CreateRunInfo, name="upload"),
    url(r'run/(?P<id>.+)/', views.SingleRunView, name="run"),
]
