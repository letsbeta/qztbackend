# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import OpenId, User, Company, UserinCompany, Job, Client

# Register your models here.
admin.site.register(OpenId)
admin.site.register(User)
admin.site.register(Company)
admin.site.register(UserinCompany)
admin.site.register(Job)
admin.site.register(Client)

