from django.db import models
import shortuuid
import hashlib


class Machine(models.Model):

	machine_id = models.BigAutoField(primary_key=True)

	add_time = models.DateTimeField(auto_now_add=True)

	alias = models.CharField(max_length=100, blank=False, default='', unique=True)

	machine_secret = models.CharField(max_length=128, blank=False, default='', unique=True)

	approved = models.BooleanField(default=False)

	owner_id = models.ForeignKey('auth.User', related_name='machines', on_delete=models.CASCADE)

	class Meta:
		ordering = ('add_time',)

	def __str__(self):
		return self.alias
