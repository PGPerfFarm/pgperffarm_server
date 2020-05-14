from django.db import models
import shortuuid
import hashlib
from django.contrib.auth.hashers import make_password

# Create your models here.

# machine = Machine(alias='test')
# machine.save()

class Alias(models.Model):
	name = models.CharField(max_length=32, unique=True, verbose_name="alias name")
	is_used = models.BooleanField(default=False,verbose_name="is_used")
	add_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class Machine(models.Model):

	ACTIVE = 'A' 
	INACTIVE = 'I'

	STATE = [
		(ACTIVE, 'Active'),
		(INACTIVE, 'Inactive'),
	]

	add_time = models.DateTimeField(auto_now_add=True)
	alias = models.CharField(max_length=100, blank=True, default='')
	machine_secret = models.CharField(max_length=32, blank=True, default='', verbose_name="machine secret")
	sn = models.CharField(max_length=16, blank=True, default='')
	os_name = models.CharField(max_length=100, blank=True, default='')
	os_version = models.CharField(max_length=100, blank=True, default='')
	comp_name = models.CharField(max_length=100, blank=True, default='')
	comp_version = models.CharField(max_length=100, blank=True, default='')
	state = models.CharField(max_length=10, choices=STATE, default=ACTIVE)
	owner_id = models.ForeignKey('auth.User', related_name='machines', on_delete=models.CASCADE)
	owner_email = models.EmailField(max_length=256, verbose_name='email')
	owner_username = models.CharField(max_length=100, blank=True, default='')

	class Meta:
		ordering = ('add_time',)

	def __str__(self):
		return self.alias
