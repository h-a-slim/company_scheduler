"""
Vacation application, URL configuration
"""

from django.conf.urls import url

from vacation import api
from vacation import views


app_name = 'vacation'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/login/', api.login, name='login'),
    url(r'^api/register/', api.login, name='register')
]
