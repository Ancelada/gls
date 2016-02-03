#!/usr/bin/python
# -*- coding: utf8 -*-
from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
	url(r'^login/$', 'login.views.login'),
	url(r'^logout/$', 'login.views.logout'),
)