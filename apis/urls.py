from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns
from apis import views

urlpatterns = [
    url(r'wxlogin$', views.wxlogin, name='wxlogin'),
    url(r'user$', views.user_update, name='user_update'),
    url(r'user/(.*)/$', views.user_detail, name='user_detail'),
    url(r'users$', views.user_list, name='user_list'),
    url(r'company$', views.company_register, name='company_register'),
    url(r'yourcompany/(.*)/$', views.get_your_company_info, name='your_company_detail'),
    url(r'companys$', views.company_list, name='company_list'),
    url(r'job$', views.job_add, name='job_add'),
    url(r'jobs$', views.job_list, name='job_list'),
    url(r'yourjobs/(.*)/$', views.job_list_by_company, name='your_jobs'),
    url(r'jobstatus/(.*)/$', views.job_status_switch, name='change_jobs_status'),
    url(r'client$', views.client_add, name='client_add'),
    url(r'yourclients/(.*)/$', views.client_get_by_company, name='your_clients'),
    url(r'clientstatus/(.*)/$', views.client_status_switch, name='client_jobs_status'),
    #url(r'adduser2company$', views.add_user_to_company, name='add_user_to_company'),
]

