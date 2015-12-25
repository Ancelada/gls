#!/usr/bin/python
# -*- coding: utf8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
	url(r'^$', 'mainapp.views.main'),
	url(ur'^query/(?P<query>[а-яА-ЯёЁA-Za-z0-9_\ _+.,-]+)$', 'mainapp.views.inputquery'),
	url(r'^getkoors/$', 'mainapp.views.getkoors'),
)