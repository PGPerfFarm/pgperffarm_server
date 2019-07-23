from django.db import models
import shortuuid
import hashlib
from django.contrib.auth.hashers import make_password

'''
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
'''

# Create your models here.

'''
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())
'''

# machine = Machine(alias='test')
# machine.save()

class Machine(models.Model):

	highlighted = models.TextField()

	ACTIVE = 'A'
	PENDING = 'P'
	INACTIVE = 'P'

	STATE = [
		(ACTIVE, 'Active'),
		(PENDING, 'Pending'),
		(INACTIVE, 'Inactive'),
	]

	added = models.DateTimeField(auto_now_add=True)
	alias = models.CharField(max_length=100, blank=True, default='')
	machine_secret = models.CharField(max_length=32, blank=True, default='', verbose_name="machine secret")
	sn = models.CharField(max_length=16, blank=True, default='')
	os_name = models.CharField(max_length=100, blank=True, default='')
	os_version = models.CharField(max_length=100, blank=True, default='')
	comp_name = models.CharField(max_length=100, blank=True, default='')
	comp_version = models.CharField(max_length=100, blank=True, default='')
	state = models.CharField(max_length=10, choices=STATE, default=PENDING)
	owner = models.ForeignKey('auth.User', related_name='machines', on_delete=models.CASCADE)

	class Meta:
		ordering = ('added',)

	def save(self, *args, **kwargs):
		"""
		Use the `pygments` library to create a highlighted HTML
		representation of the code snippet.
		"""
		#lexer = get_lexer_by_name(self.language)
		#alias = 'table' if self.alias else False
		#options = {'title': self.title} if self.title else {}
		#formatter = HtmlFormatter(style=self.style, linenos=linenos, full=True, **options)
		#self.highlighted = highlight(self.code, lexer, formatter)

		self.machine_sn = shortuuid.ShortUUID().random(length=16)

		machine_str = self.alias + self.os_name + self.os_version + self.comp_name + self.comp_version + self.machine_sn

		m = hashlib.md5()
		m.update(make_password(str(machine_str), 'pg_perf_farm').encode('utf-8'))
		self.machine_secret = m.hexdigest()

		super(Machine, self).save(*args, **kwargs)
