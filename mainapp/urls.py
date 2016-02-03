#!/usr/bin/python
# -*- coding: utf8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
	url(r'^$', 'mainapp.views.main'),

	url(r'^send_json_request$', 'mainapp.views.send_json_request'),
	url(r'^recieve_json$', 'mainapp.views.recieve_json'),

	#receive slmp
	url(r'^send_simple_location_message$', 'mainapp.views.send_simple_location_message'),
	url(r'^receive_slmp$', 'mainapp.views.receive_slmp'),
	url(r'^save_slmp$', 'mainapp.views.save_slmp'),

	#get location
	url(r'getxyzvalues$', 'mainapp.views.getxyzvalues'),

	#3d practice
	url(r'landscape$', 'mainapp.views.landscape'),
	url(r'movement$', 'mainapp.views.movement'),
	url(r'children$', 'mainapp.views.children'),
	url(r'loadcollada$', 'mainapp.views.loadcollada'),

	#get ajax marks count
	url(r'getmarksvalues', 'mainapp.views.getmarksvalues'),
	url(r'getmarks', 'mainapp.views.getmarks'),

	#scene view
	url(ur'values/(?P<landscape_id>[а-яА-ЯёЁA-Za-z0-9_\ _+.,-]+)$', 'mainapp.views.values'),

	#landscape load
	url(ur'landscapeloadform/(?P<result>[а-яА-ЯёЁA-Za-z0-9_\ _+.,-]+)$', 'mainapp.views.landscapeloadform'),

	#landscape elems tree to database
	url(ur'landscapetreeload/(?P<landscape_id>[а-яА-ЯёЁA-Za-z0-9_\ _+.,-]+)$', 'mainapp.views.landscapetreeload'),
	url(r'landscape_save$', 'mainapp.views.landscape_save'),
	
	#min max interval to session
	url(r'minmaxtosession$', 'mainapp.views.minmaxtosession'),

	#testing sockjs
	url(r'sockjs$', 'mainapp.views.sockjs'),
	url(r'orderadd$', 'mainapp.views.orderadd'),
	url(r'getsessions$', 'mainapp.views.getsessions'),
	url(r'setproperty$', 'mainapp.views.setproperty'),

	#testing
	url(r'testing$', 'mainapp.views.testing'),
)