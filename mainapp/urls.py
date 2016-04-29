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
	url(r'^receive_slmp$', 'mainapp.views.receive_slmp'),

	#get location
	url(r'getxyzvalues$', 'mainapp.views.getxyzvalues'),

	#3d practice
	url(r'landscape$', 'mainapp.views.landscape'),
	url(r'movement$', 'mainapp.views.movement'),
	url(r'children$', 'mainapp.views.children'),
	url(r'loadcollada$', 'mainapp.views.loadcollada'),

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

	#send coordinates
	url(r'sendcoordsform', 'mainapp.views.sendcoordsform'),

	#unique
	url(r'clearunique', 'mainapp.views.clearUnique'),
	url(r'getuniquevalues', 'mainapp.views.getuniquevalues'),
	url(ur'getuval/(?P<parameters>[а-яА-ЯёЁA-Za-z0-9_\ _+.,-]+)$', 'mainapp.views.getuniquevalues2'),

	url(ur'values_server/(?P<landscape_id>[а-яА-ЯёЁA-Za-z0-9_\ _+.,-]+)$', 'mainapp.views.values_server'),

	#static
	url(r'getstatic', 'mainapp.views.getstatic'),
	url(r'turnoff_tumbler', 'mainapp.views.turnoff_tumbler'),
	url(r'clearstatic', 'mainapp.views.clearstatic'),

	#reports
	url(r'simplereport/(?P<parameters>[0-1]+)', 'mainapp.views.simplereport'),

	#matrix
	# url(r'matrix', 'mainapp.views.matrix'),

	#testing match
	url(r'match', 'mainapp.views.match'),

	#active_users
	url(r'getactiveusers', 'mainapp.views.getactiveusers'),

	#object name define module - buildings, floors, etc
	url(r'definemain/(?P<parameters>[0-9]+)', 'mainapp.views.definemain'),
	#Tag in out group
	url(r'taginoutgroup/(?P<group>[0-9]+)', 'mainapp.views.taginoutgroup'),
	#TagGroup manager
	url(r'taggroupmanager', 'mainapp.views.taggroupmanager'),
	#TagGroup mesh define module
	url(r'definetaggroup/(?P<parameters>[0-9]+)/(?P<geomtype>\w+)', 'mainapp.views.definetaggroup'),
	#register tag module
	url(ur'tagregister/(?P<tag_id>[а-яА-ЯёЁA-Za-z0-9_\ _+.,-]+)$', 'mainapp.views.tagregister'),


	#income zone define
	url(ur'incomezonedefine/(?P<landscape_id>[а-яА-ЯёЁA-Za-z0-9_\ _+.,-]+)$', 'mainapp.views.incomezonedefine'),

	#unique belong
	url(r'getbelong$', 'mainapp.views.getbelong'),

	#unique belong to uzone
	url(r'getbelonguzone$', 'mainapp.views.getbelonguzone'),

	#show userzones by landscape_id
	url(r'getuzones/(?P<parameters>[0-9]+)', 'mainapp.views.getuzones'),

	# работа с роутерами, координаторами и т. д.
	url(r'getobjectlistfromserver', 'mainapp.views.getobjectlistfromserver'),
	# работа с сессиями
	# информация от SP
	url(r'getsessionsfromserver', 'mainapp.views.getsessionsfromserver'),
	# информация от WS
	url(r'getmysession', 'mainapp.views.getmysession'),
)