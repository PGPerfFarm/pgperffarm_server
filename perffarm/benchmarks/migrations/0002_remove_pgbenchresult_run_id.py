# Generated by Django 3.2.13 on 2023-05-06 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('benchmarks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pgbenchresult',
            name='run_id',
        ),
    ]