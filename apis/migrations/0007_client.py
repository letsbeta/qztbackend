# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-28 14:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0006_job_register_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('register_by', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=1)),
                ('update_at', models.DateTimeField(verbose_name='date updated')),
            ],
        ),
    ]