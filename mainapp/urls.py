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
	url(r'^receive_slmp$', 'mainapp.views.receive_slmp'),
	url(r'^save_slmp$', 'mainapp.views.save_slmp'),

	url(r'landscape$', 'mainapp.views.landscape'),

	url(r'getxyzvalues$', 'mainapp.views.getxyzvalues'),


	url(r'movement$', 'mainapp.views.movement'),

	url(r'children$', 'mainapp.views.children'),

	url(r'delete$', 'mainapp.views.delete'),
)