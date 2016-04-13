#!/usr/bin/python
# -*- coding: utf8 -*-
from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
	#reportsselect page
	url(r'reportselect', 'report.views.reportselect'),
	url(r'reportparameters/(?P<report>[0-9]+)$', 'report.views.reportparameters'),
)