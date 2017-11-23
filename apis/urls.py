from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns
from apis import views

urlpatterns = [
    url(r'docs$', views.api_root, name='api_root'),

    url(r'iplookup$', views.api_iplookup, name='iplookup'),
    url(r'location$', views.api_location, name='location'),

    url(r'wxlogin$', views.wxlogin, name='wxlogin'),

    # user operations
    url(r'user$', views.user_create_or_update, name='user_create_or_update'),
    url(r'user/(.*)/$', views.user_detail, name='user_detail'),
    url(r'users$', views.user_list, name='user_list'),

    # company operations
    url(r'company$', views.company_create_or_update, name='company_create_or_update'),
    url(r'yourcompany/(.*)/$', views.get_your_company_info, name='get_your_company_info'),
    url(r'companys$', views.company_list, name='company_list'),

    # job operations
    url(r'job$', views.job_create, name='job_create'),
    url(r'jobs$', views.job_list, name='job_list'),
    url(r'yourjobs/(.*)/$', views.get_your_company_jobs, name='get_your_company_jobs'),
    url(r'jobstatus/(.*)/$', views.toggle_job_status, name='toggle_job_status'),

    # clients operations
    url(r'client$', views.client_create, name='client_create'),
    url(r'yourclients/(.*)/$', views.get_your_company_clients, name='get_your_company_clients'),
    url(r'clientstatus/(.*)/$', views.toggle_client_status, name='toggle_client_status'),

    # misc
    url(r'userjoin$', views.add_user_to_company, name='add_user_to_company'),
]

