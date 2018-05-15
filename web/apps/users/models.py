from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserProfile(AbstractUser):
    """
    user
    """
    # first_name = None
    # last_name = None
    # user_name = models.CharField(max_length=64, verbose_name="name")
    # user_email = models.EmailField(max_length=256, verbose_name="email")
    # add_time = models.DateTimeField(default=datetime.now, verbose_name="user added time")

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "user"

    def __str__(self):
        return self.user_name

