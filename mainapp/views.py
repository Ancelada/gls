#!/usr/bin/python
# -*- coding: utf8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from mainapp.models import Metka, Std0
from django.db.models import Q
import json
import requests
from django.http import StreamingHttpResponse
try:
	from urllib.request import urlopen
	from urllib.parse import urljoin
except ImportError:
	from urllib2 import urlopen	
	from urlparse import urljoin
import ssl
import datetime

#модули асинхронного сервера
import redis
from django.conf import settings
from django.db import models
import simplejson

ORDERS_FREE_LOCK_TIME = getattr(settings, 'ORDERS_FREE_LOCK_TIME', 0)
ORDERS_REDIS_HOST = getattr(settings, 'ORDERS_REDIS_HOST', 'localhost')
ORDERS_REDIS_PORT = getattr(settings, 'ORDERS_REDIS_PORT', 6379)
ORDERS_REDIS_PASSWORD = getattr(settings, 'ORDERS_REDIS_PASSWORD', None)
ORDERS_REDIS_DB = getattr(settings, 'ORDERS_REDIS_DB', None)

service_queue = redis.StrictRedis(
	host = ORDERS_REDIS_HOST,
	port = ORDERS_REDIS_PORT,
	db = ORDERS_REDIS_DB,
	password = ORDERS_REDIS_PASSWORD
).publish

json = simplejson.dumps

def lock(self):
	"""
	Закрепление заказа
	"""
	service_queue('order_lock', json({
		'user': self.client.pk,
		'order': self.pk,	
	}))

def done(self):
	"""
	Завершение заказа
	"""
	service_queue('order_done', json({
		'user': self.client.pk,
		'order': self.pk,	
	}))

def sockjs(request):
	return render(request, 'sockjs.html')

# Глобальный словарь с метками
massive = {}

def main(request):
	return render(request, 'metka.html')

def send_json_request(request):
	url = 'http://localhost:8000/recieve_json'
	data = {'data':[{'key1': 'val1'}, {'key2': 'val2'}]}
	headers = {'content-type': 'application/json'}
	r = requests.post(url, data=json.dumps(data), headers=headers)
	return redirect('/')

def recieve_json(request):
	if request.method == 'POST':
		Metka(text=json.loads(request.body)).save()



def send_simple_location_message(request):
	slmp = """LabR,Std0,0000,00000a5,10.681625,10.457092,10.803710,7,2016-01-13T13:52:31:239+1,2,0038,0000
	LabR,Std0,0000,00000a6,15.681625,15.457092,15.803710,7,2016-01-13T13:52:31:239+1,2,0038,0000
	LabR,Std0,0000,00000a7,25.681625,25.457092,25.803710,7,2016-01-13T13:52:31:239+1,2,0038,0000
	LabR,Std0,0000,00000a7,35.681625,35.457092,35.803710,7,2016-01-13T13:52:31:239+1,2,0038,0000
	LabR,Std0,0000,00000a7,45.681625,45.457092,45.803710,7,2016-01-13T13:52:31:239+1,2,0038,0000
"""
	url = 'http://localhost:8000/receive_slmp'
	r = requests.post(url, data=slmp)
	return redirect('/')


def receive_slmp(request):
	if request.method == 'POST':
		# в глобальный список
		line = request.body.decode('utf-8')
		massive['data'] = line
		return HttpResponse('ok')
	return HttpResponse('ok')

def save_slmp(request):
	if request.method == 'POST':
		queryset = list(Std0.objects.raw("""
			select *, max(DateImport) as Date from Metka
			where readed is null"""))
		try:
			line = queryset[0].text.decode('utf-8')
		except:
			return HttpResponse('Nothing to parse')
		line = line.split('Zone')
		if (len(line) > 1):
			Metka(text=line[2].replace('\n', '')).save()
			line = line[2]
			line = line.split(',')
			Std0(LabD=line[0], Std0=line[1], Tag_ID_Format=line[2], Tag_ID=line[3], X=line[4], Y=line[5], Z=line[6], Zone=line[7], DateImport=datetime.datetime.now()).save()

			#отметка что данная пачка распарсена
			mrk = queryset[0].DateImport
			a = Metka.objects.filter(DateImport=mrk).update(readed=True)
			return HttpResponse('received')
		else:
			line = line[0].split('\n')
			for i in line:
				try:
					line = i.split(',')
					Std0(LabD=line[0], Std0=line[1], Tag_ID_Format=line[2], Tag_ID=line[3], X=line[4], Y=line[5], Z=line[6], Zone=line[7], Timestamp=line[8], DateImport=datetime.datetime.now()).save()
					#отметка что данная пачка распарсена
					mrk = queryset[0].DateImport
					a = Metka.objects.filter(DateImport=mrk).update(readed=True)
				except:
					return HttpResponse('received')
		return HttpResponse('received')

def landscape(request):
	return render(request, 'landscape.html')

def getxyzvalues(request):
	if request.method == 'POST':
		queryset = list(Std0.objects.raw("""
			select *, max(DateImport) as Date from Std0
			group by Tag_ID
			"""))
		Str = ''
		num = 0
		for tag_id in queryset:
			if num < len(queryset) - 1:
				Str += '(Tag_ID="%s" and DateImport="%s") or ' %(tag_id.Tag_ID, tag_id.Date)
			else:
				Str += '(Tag_ID="%s" and DateImport="%s")' %(tag_id.Tag_ID, tag_id.Date)
			num+=1
		Str = Str.replace('"', "'")
		queryset2 = list(Std0.objects.raw("""
			select * from Std0
			where %s
			""" % Str))
		marks = {}
		num = 0
		for i in queryset2:
			spisok = []
			spisok.append({'tag_id':i.Tag_ID, 'x': i.X, 'y': i.Y, 'z': i.Z})
			marks[num] = spisok
			num+=1
	return JsonResponse(marks)

def movement(request):
	return render(request, 'movement.html')

def children(request):
	return render(request, 'children.html')

def loadcollada(request):
	return render(request, 'loadcollada.html')

def values(request):
	return render(request, 'values.html')

def getmarksvalues(request):
	if request.method == 'POST':
		marks = {}
		line = massive['data']
		line = line.split('Zone')
		num = 0
		if (len(line) > 1):
			line = line[2]
			line = line.split(',')
			for i in line:
				spisok = []
				spisok.append({'tag_id':line[3], 'x': line[4], 'y': line[5], 'z': line[6], 'zone':[8]})
				marks[num] = spisok
			return JsonResponse(marks)
		else:
			line = line[0].split('\n')
			for i in line:
				try:
					line = i.split(',')
					spisok = []
					spisok.append({'tag_id':line[3], 'x': line[4], 'y': line[5], 'z': line[6], 'zone':line[8]})
					marks[num] = spisok
					num +=1
				except:
					pass
			return JsonResponse(marks)