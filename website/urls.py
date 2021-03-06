__author__ = 'parth'
"""settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^$', csrf_exempt(home), name='home'),
    url(r'^board/$', show_billboard, name='show_billboard'),
    url(r'^board/(?P<bid>[-\w]+)/$', csrf_exempt(show_billboard) , name='show_billboard'),
    url(r'^explore/$', csrf_exempt(explore_more)),
    url(r'^image_data/$', csrf_exempt(image_data)),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
]
