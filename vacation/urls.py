"""
Vacation application, URL configuration
"""

from django.conf.urls import url

from vacation import api
from vacation import views


app_name = 'vacation'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^schedule/$', views.schedule, name='schedule'),
    url(r'^api/signin/', api.signin, name='signin'),
    url(r'^api/register/', api.register, name='register'),
    url(r'^api/duration/', api.duration, name='duration'),
    url(r'^api/apply/', api.apply, name='apply'),
    url(r'^api/employee_vacations/', api.employee_vacations, name='employee_vacations')
]
