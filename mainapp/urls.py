#!/usr/bin/python
# -*- coding: utf8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
	url(r'^$', 'mainapp.views.main'),

	url(r'^send_json_request$', 'mainapp.views.send_json_request'),
	url(r'^recieve_json$', 'mainapp.views.recieve_json'),

	url(r'^send_simple_location_message$', 'mainapp.views.send_simple_location_message'),
	url(ur'^receive_slmp/(?P<slmp>[а-яА-ЯёЁA-Za-z0-9_\ _+.,-]+)$', 'mainapp.views.receive_slmp'),
)