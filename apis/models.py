# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible
class OpenId(models.Model):
    openid = models.CharField(max_length=64)
    update_at = models.DateTimeField('date updated')

    def __str__(self):
        return self.openid

@python_2_unicode_compatible
class User(models.Model):
    openid = models.CharField(max_length=64)
    avatar = models.CharField(max_length=256)
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    gender = models.IntegerField(default=1)
    nickname = models.CharField(max_length=128)
    province = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=32)
    birthday = models.CharField(max_length=32)
    hidden = models.IntegerField(default=0)
    role = models.IntegerField(default=0x1)
    intro = models.CharField(max_length=256, blank=True, default='')
    idcard = models.CharField(max_length=32, blank=True, default='')
    address = models.CharField(max_length=128, blank=True, default='')
    create_at = models.DateTimeField('date created')
    update_at = models.DateTimeField('date updated')

    def __str__(self):
        return self.name + ' ' + self.phone

@python_2_unicode_compatible
class Company(models.Model):
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=32)
    address = models.CharField(max_length=64)
    intro = models.CharField(max_length=256)
    #who edit this message, openid of the editor
    register_by = models.CharField(max_length=64)
    update_at = models.DateTimeField('date updated')
    #status: 0, invalid 1, processing 2, success
    status = models.IntegerField(default=1)
    def __str__(self):
        return self.name


@python_2_unicode_compatible
class UserinCompany(models.Model):
    openid = models.CharField(max_length=64)
    companyid = models.IntegerField(default=0)

    def __str__(self):
        return 'User %s in Company %d' %(self.openid, self.companyid)

@python_2_unicode_compatible
class Job(models.Model):
    name = models.CharField(max_length=32)
    low = models.IntegerField(default=0)
    high = models.IntegerField(default=0)
    city = models.CharField(max_length=16)
    district = models.CharField(max_length=16)
    title = models.CharField(max_length=16)
    phone = models.CharField(max_length=32)
    intro = models.CharField(max_length=256)
    update_at = models.DateTimeField('date updated')
    status = models.IntegerField(default=1) #0 hidden, 1 show
    register_by = models.IntegerField(default=0); #company id

    def __str__(self):
        return '%s %s' %(self.name, self.title)


@python_2_unicode_compatible
class Client(models.Model):
    name = models.CharField(max_length=32)
    register_by = models.IntegerField(default=0)    #company who add it
    status = models.IntegerField(default=1) # 0 hidden, 1 show
    update_at = models.DateTimeField('date updated')

    def __str__(self):
        return '%s by %d' % (self.name, self.register_by)

