from django.db import models
from django.core import validators


# Create your models here.
class EmailNotification(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_active = models.BooleanField(default=False)
    threshold = models.IntegerField(default=20, validators=[validators.MinValueValidator(1), validators.MaxValueValidator(99)])
    type = models.ForeignKey('benchmarks.BenchmarkType', on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
