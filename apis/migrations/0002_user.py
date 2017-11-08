# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-18 09:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openid', models.CharField(max_length=64)),
                ('avatar', models.CharField(max_length=256)),
                ('city', models.CharField(max_length=64)),
                ('country', models.CharField(max_length=64)),
                ('gender', models.IntegerField(default=1)),
                ('nickname', models.CharField(max_length=128)),
                ('province', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('phone', models.CharField(max_length=32)),
                ('birthday', models.CharField(max_length=32)),
                ('hidden', models.IntegerField(default=0)),
                ('role', models.IntegerField(default=1)),
                ('intro', models.CharField(blank=True, default='', max_length=256)),
                ('idcard', models.CharField(blank=True, default='', max_length=32)),
                ('address', models.CharField(blank=True, default='', max_length=128)),
                ('create_at', models.DateTimeField(verbose_name='date created')),
                ('update_at', models.DateTimeField(verbose_name='date updated')),
            ],
        ),
    ]