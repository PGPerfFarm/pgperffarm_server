from django.conf.urls import url

from pages import views

urlpatterns = [
    url('', views.index, name='index'),
]
