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
	owner = models.ForeignKey('auth.User', related_name='machines', on_delete=models.CASCADE)

	class Meta:
		ordering = ('add_time',)

	def save(self, *args, **kwargs):

		alias = Alias.objects.filter(is_used=False).order_by('?').first()
		if not alias:
			return {"is_success": False, "alias": '', "secret": '', "email":''}

		from django.db import transaction
		with transaction.atomic():
			alias.is_used = True
			alias.save()

			self.alias = alias['name']
			self.state = 1

		if not self.machine_sn:
			self.sn = shortuuid.ShortUUID().random(length=16)

		if not self.machine_secret:
			machine_str = self.alias + self.os_name + self.os_version + self.comp_name + self.comp_version + self.sn

		m = hashlib.md5()
		m.update(make_password(str(machine_str), 'pg_perf_farm').encode('utf-8'))
		self.machine_secret = m.hexdigest()

		self.save()

		print(self.machine_owner.email)
		user_email = self.machine_owner.email
		system = self.os_name + ' ' + self.os_version
		compiler = self.comp_name + ' ' + self.comp_version
		return  {"is_success": True, "alias": self.alias.name, "secret": self.machine_secret, "system": system,  "compiler":compiler,"email":user_email}

