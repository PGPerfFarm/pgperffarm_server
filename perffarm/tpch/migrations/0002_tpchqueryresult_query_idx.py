# Generated by Django 3.2.13 on 2023-06-16 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tpch', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tpchqueryresult',
            name='query_idx',
            field=models.SmallIntegerField(default=1),
        ),
    ]
