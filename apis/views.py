# 2017.11.08 16:07:18 CST
#Embedded file name: /home/ubuntu/django-project/qztbackend/apis/views.py
from django.http import Http404
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from apis.models import OpenId, User, Company, UserinCompany, Job, Client
from apis.serializers import UserSerializer, CompanySerializer, JobSerializer, ClientSerializer
import json
import requests
import logging
logger = logging.getLogger('qzt')
APP_SECRET = 'd8af9299cc650a4f6d045106c45ce76f'
APP_ID = 'wx2394a55a588a27c1'
SECRET_KEY = 'itisreallyhard2guess!'

def get_openid(code):
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    payload = {'appid': APP_ID,
     'secret': APP_SECRET,
     'js_code': code,
     'grant_type': 'authorization_code'}
    r = requests.post(url, params=payload)
    return r.json()


def pagination(size, request, objs, seria):
    offset = 0
    if 'offset' in request.query_params:
        offset = int(request.query_params['offset'])
    count = len(objs)
    next = '?offset={}'.format(offset + size) if offset + size < count else ''
    serializer = seria(objs[offset:offset + size], many=True)
    return (serializer, next)


@api_view(['POST'])
def wxlogin(request, format = None):
    """
    Interface to get weixin openid
    """
    rq = request.data
    logger.info(rq)
    res = get_openid(rq['code'])
    logger.info(res)
    status = 200
    if 'errcode' in res:
        status = 400
    if status == 200:
        o = OpenId.objects.filter(openid=res['openid']).first()
        if not o:
            o = OpenId(openid=res['openid'], update_at=timezone.now())
            o.save()
    return Response(res, status=status)


@api_view(['POST'])
def user_update(request, format = None):
    """
    Create/update a user's detail info into database
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    rq = request.data
    logger.info(rq)
    u = User.objects.filter(openid=rq['openid']).first()
    if u:
        create_at = u.create_at
    else:
        create_at = timezone.now()
    defaults = {'avatar': rq['avatarUrl'],
     'city': rq['city'],
     'country': rq['country'],
     'gender': rq['genderx'],
     'nickname': rq['nickName'],
     'province': rq['province'],
     'name': rq['name'],
     'phone': rq['phone'],
     'birthday': rq['birthday'],
     'intro': rq['intro'],
     'create_at': create_at,
     'update_at': timezone.now()}
    obj, created = User.objects.update_or_create(openid=rq['openid'], defaults=defaults)
    serializer = UserSerializer(obj)
    return Response(serializer.data)


@api_view(['GET'])
def user_detail(request, openid, format = None):
    """
    Get a user's detail info from database
    """
    u = User.objects.filter(openid=openid).first()
    if not u:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializer(u)
    return Response(serializer.data)


@api_view(['GET'])
def user_list(request, format = None):
    """
    Return the user list
    """
    users = User.objects.all().order_by('-update_at')
    serializer, next = pagination(10, request, users, UserSerializer)
    return Response({'users': serializer.data,
     'next': next})


@api_view(['POST'])
def company_register(request, format = None):
    """
    Register or update a company infomation
    """
    rq = request.data
    if 'company_id' not in rq:
        logger.info('create new company %s' % rq)
        c = Company(name=rq['name'], phone=rq['phone'], address=rq['address'], intro=rq['intro'], register_by=rq['openid'], update_at=timezone.now())
        c.save()
    else:
        logger.info('update existing company %s' % rq)
        defaults = {'name': rq['name'],
         'phone': rq['phone'],
         'address': rq['address'],
         'intro': rq['intro'],
         'register_by': rq['openid'],
         'update_at': timezone.now()}
        c, create = Company.objects.update_or_create(id=rq['company_id'], defaults=defaults)
    defaults = {'companyid': c.id}
    obj, _ = UserinCompany.objects.update_or_create(openid=rq['openid'], defaults=defaults)
    serializer = CompanySerializer(c)
    return Response(serializer.data)


@api_view(['GET'])
def get_your_company_info(request, openid, format = None):
    """
    Get user's company info
    """
    rl = UserinCompany.objects.filter(openid=openid).first()
    if not rl:
        return Response(status=status.HTTP_404_NOT_FOUND)
    companyid = rl.companyid
    com = Company.objects.filter(id=companyid).first()
    if not com:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CompanySerializer(com)
    return Response(serializer.data)


@api_view(['GET'])
def company_list(request, format = None):
    """
    Return list of company
    """
    c = Company.objects.all()
    serializer = CompanySerializer(c, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def job_add(request, format = None):
    """
    Add new job
    """
    rq = request.data
    j = Job(name=rq['name'], low=rq['low'], high=rq['high'], city=rq['city'], district=rq['district'], title=rq['title'], phone=rq['phone'], intro=rq['intro'], update_at=timezone.now(), register_by=rq['company_id'])
    j.save()
    serializer = JobSerializer(j)
    return Response(serializer.data)


@api_view(['GET'])
def job_list(request, format = None):
    """
    List all the jobs
    """
    j = Job.objects.filter(status=1).order_by('-update_at')
    serializer, next = pagination(10, request, j, JobSerializer)
    return Response({'jobs': serializer.data,
     'next': next})


@api_view(['GET'])
def job_list_by_company(request, company_id, format = None):
    """
    List all jobs filed by your company
    """
    j = Job.objects.filter(register_by=company_id, status=1).order_by('-update_at')
    serializer = JobSerializer(j, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def job_status_switch(request, job_id, format = None):
    """
    Toggle job status hidden or show
    """
    try:
        j = Job.objects.get(id=job_id)
        rq = request.data
        j.status = rq['status']
        j.save()
        return Response(status=status.HTTP_200_OK)
    except Job.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def client_add(request, format = None):
    """
    Add client
    """
    rq = request.data
    client = Client(name=rq['name'], register_by=rq['company_id'], update_at=timezone.now())
    client.save()
    clients = Client.objects.filter(register_by=rq['company_id'], status=1)
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def client_get_by_company(request, company_id, format = None):
    """
    Get clients belongs to company
    """
    clients = Client.objects.filter(register_by=company_id, status=1)
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def client_status_switch(request, client_id, format = None):
    """
    Toggle client status hidden or show
    """
    try:
        c = Client.objects.get(id=client_id)
        rq = request.data
        c.status = rq['status']
        c.save()
        clients = Client.objects.filter(register_by=rq['company_id'], status=1)
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_user_to_company(request, format = None):
    """
    User is added as employee
    """
    rq = request.data
    cid = rq['company_id']
    defaults = {'companyid': cid}
    obj, _ = UserinCompany.objects.update_or_create(openid=rq['openid'], defaults=defaults)
    return Response(status=status.HTTP_200_OK)
+++ okay decompyling /home/ubuntu/views.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2017.11.08 16:07:18 CST
