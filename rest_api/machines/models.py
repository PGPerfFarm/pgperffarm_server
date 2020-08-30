from django.db import models
import hashlib


class Machine(models.Model):

	machine_id = models.BigAutoField(primary_key=True)

	add_time = models.DateTimeField(auto_now_add=True)

	alias = models.CharField(max_length=100, blank=False, default='', unique=True)

	description = models.CharField(max_length=200, blank=True, default='', unique=False, null=True)

	machine_secret = models.CharField(max_length=128, blank=False, default='', unique=True)

	approved = models.BooleanField(default=False)

	owner_id = models.ForeignKey('auth.User', related_name='machines', on_delete=models.CASCADE)

	machine_type = models.CharField(max_length=100, blank=False, default='')

	class Meta:
		ordering = ('add_time',)

	def __str__(self):
		return self.alias


class MachineManager(models.Manager):
	
    def get_by_natural_key(self, machine_id, add_time, alias, description, machine_secret, approved, owner_id):
        return self.get(machine_idh=machine_id, add_time=add_time, alias=alias, description=description, machine_secret=machine_secret, approved=approved, owner_id=owner_id)
