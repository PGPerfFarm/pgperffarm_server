from django.conf.urls import url

from email_notification import views

app_name = "email_notification"

urlpatterns = [
    url('update_email_notification', views.update_email_notification_view, name='update_email_notification')
    ]

