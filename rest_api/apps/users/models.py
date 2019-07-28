from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

class User(AbstractBaseUser):

	username = models.CharField(max_length=64, unique=True, verbose_name="username")
	email = models.EmailField(max_length=256, verbose_name="email", unique=True)

	USERNAME_FIELD = 'username'
	
	# eventually add __str__
