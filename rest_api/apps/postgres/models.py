from django.db import models
import shortuuid
import hashlib


class PostgresInfo(models.Model):

	# automatic id
	info = JsonField()
	hash = CharField(max_length=1000, unique=True, blank=False)


class PostgresSettingsSet(models.Model):

	settings_sha256 = models.BinaryField(max_length=256)


class PostgresSettings(models.Model):

	db_settings_id = models.ForeignKey(PostgresSettingsSet)

	setting_name = models.TextField(blank=False)
	setting_unit = models.TextField()
	setting_value = models.TextField()

	class Meta:
    unique_together = ('db_settings_id', 'setting_name',)





