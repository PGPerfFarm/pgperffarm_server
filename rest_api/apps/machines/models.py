from django.db import models
#from pygments.lexers import get_all_lexers
#from pygments.styles import get_all_styles

# Create your models here.

'''
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())
'''

#snippet = Snippet(code='foo = "bar"\n')
#snippet.save()

class Machine(models.Model):

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
	sn = models.TextField()
	os_name = models.CharField(max_length=100, blank=True, default='')
	os_version = models.CharField(max_length=100, blank=True, default='')
	comp_name = models.CharField(max_length=100, blank=True, default='')
	comp_version = models.CharField(max_length=100, blank=True, default='')
	reports = models.IntegerField(default=0)
	lastest = models.CharField(max_length=100, blank=True, default='')
	state = models.CharField(max_length=10, choices=STATE, default=PENDING)

	class Meta:
		ordering = ('added',)
