from django.core.mail import send_mail
from rest_api.settings_local import *


def send_the_email(recipents, subject, message):
    send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=recipents
    )