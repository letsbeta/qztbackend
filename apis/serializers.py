# -*- coding: utf-8 -*-
from django.utils import timezone
from rest_framework import serializers
from apis.models import User, Company, Job, Client

class UserSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = '__all__'

    def get_age(self, obj):
        return timezone.now().year-int(obj.birthday.split('-')[0])

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    by_company = serializers.SerializerMethodField()
    short_date = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = '__all__'

    def get_by_company(self, obj):
        try:
            com = Company.objects.get(id=obj.register_by)
            return com.name
        except Company.DoesNotExist:
            return u'未知'

    def get_short_date(self, obj):
        return str(obj.update_at).split(' ')[0]

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


