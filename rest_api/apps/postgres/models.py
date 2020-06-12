from django.db import models
import shortuuid
import hashlib


class PostgresSettingsSet(models.Model):

	postgres_settings_set_id = models.AutoField(primary_key=True)

	settings_sha256 = models.BinaryField(max_length=256)


class PostgresSettings(models.Model):

	postgres_settings_id = models.AutoField(primary_key=True)

	db_settings_id = models.ForeignKey(PostgresSettingsSet)

	setting_name = models.TextField(blank=False)
	setting_unit = models.TextField()
	setting_value = models.TextField()

	class Meta:
		unique_together = ('db_settings_id', 'setting_name',)





