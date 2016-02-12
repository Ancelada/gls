#!/usr/bin/python
# -*- coding: utf8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from mainapp.models import Metka, Std0, LoadLandscape, Building, Floor, Kabinet_n_Outer, Wall, Order
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
from django.contrib import auth
from django.conf import settings

# Глобальный словарь с метками
marks = {}

# Глобальный словарь усредненный
unique = []
tumbler = []

# global user massive 
active_users = []

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
# 	slmp = """LabR,Std0,0000,00000a5,21.681625,55.457092,10.803710,7,2016-01-12T13:52:31:239+1,2,0038,0000
# 	LabR,Std0,0000,00000a6,29.681625,49.457092,13.503710,7,2016-01-12T13:52:31:239+1,2,0038,00000a6
# 	LabR,Std0,0000,00000a7,25.681625,25.457092,25.803710,7,2016-01-12T13:52:31:239+1,2,0038,0000
# 	LabR,Std0,0000,00000a8,35.681625,35.457092,35.803710,7,2016-01-12T13:52:31:239+1,2,0038,0000
# 	LabR,Std0,0000,00000a9,45.681625,45.457092,45.803710,7,2016-01-12T13:52:31:239+1,2,0038,0000
# """
	if request.method == 'POST':
		string = simplejson.loads(request.body)
		value = string['value']
		url = 'http://localhost:8000/receive_slmp'
		r = requests.post(url, data=value)
		return JsonResponse({'value': value})

def getmarks(request):
	return HttpResponse(marks)

#unique корректировка
def clearUnique(request):
	unique = []
	return HttpResponse('unique dictionary cleared')
def getuniquevalues(request):
	return HttpResponse(unique)

# функция setInterval
import threading
def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def correctF():
	for i in unique:
		xCur = i['x']
		yCur = i['y']
		zCur = i['z']

		xNew = i['xNew']
		yNew = i['yNew']
		zNew = i['zNew']

		step = 0.1
		if (xCur < xNew + step) and ((xNew - xCur) > 0):
			i['x'] += step
	        if (yCur < yNew + step) and ((yNew - yCur) > 0):
	        	i['y'] += step
	        if (zCur < zNew + step) and ((zNew - zCur) > 0):
	        	i['z'] += step
	        if (xCur > xNew + step) and ((xNew - xCur) < 0):
	            i['x'] -= step
	        if (yCur > yNew + step) and ((yNew - yCur) < 0):
	        	i['y'] -= step
	        if (zCur > zNew + step) and ((zNew - zCur) < 0):
	        	i['z'] -= step
    	if (yCur < yNew + step) and ((yNew - yCur) > 0):
        	i['y'] += step
        	if (xCur < xNew + step) and ((xNew - xCur) > 0):
				i['x'] += step
        	if (zCur < zNew + step) and ((zNew - zCur) > 0):
	        	i['z'] += step
	        if (xCur > xNew + step) and ((xNew - xCur) < 0):
	            i['x'] -= step
	        if (yCur > yNew + step) and ((yNew - yCur) < 0):
	        	i['y'] -= step
	        if (zCur > zNew + step) and ((zNew - zCur) < 0):
	        	i['z'] -= step
    	#send coordinates to usersession
	for i in active_users:
		try:
			service_queue('coords_server_lock', json({'user': i['id'],'data': unique}))
		except:
			pass

def correctUniqueInMilisec():
	if tumbler[0]:
		set_interval(correctF, 0.1)

def values_server(request, landscape_id='0000'):
	args = {}
	landscape_id = landscape_id
	args['link'] = LoadLandscape.objects.get(landscape_id=landscape_id).landscape_source
	args['buildings'] = Building.objects.filter(LoadLandscape_id=landscape_id)
	args['floors'] = Floor.objects.filter(LoadLandscape_id=landscape_id)
	args['kabinet_n_outer'] = Kabinet_n_Outer.objects.filter(LoadLandscape_id=landscape_id)
	args['walls'] = Wall.objects.filter(LoadLandscape_id=landscape_id)
	args['username'] = auth.get_user(request).id
	args['landscape_id'] = landscape_id
	return render(request, 'values_server.html', args)

#receive coordinates
def receive_slmp(request):
	if request.method == 'POST':
		update_active_users()
		line = request.body.decode('utf-8')
		line = line.split('Zone')
		# first line
		if (len(line) > 1):
			line = line[2]
			line = line.split(',')
			for i in line:
				dictionary = {'tag_id':line[3], 'x': float(line[4]), 'y': float(line[5]), 'z': float(line[6]), 'zone':line[8], 'zone_id': line[11]}
				spisok.append(dictionary)
				getMarksByInterval(line[4], line[5], line[6], line[11], dictionary)
		# second and other lines
		else:
			line = line[0].split('\r\n')
			for i in line:
				line = i.split(',')
				if len(line) > 0:
					dictionary = {'tag_id':line[3], 'x': float(line[4]), 'y': float(line[5]), 'z': float(line[6]), 'zone':line[8], 'zone_id': line[11]}
					getMarksByInterval(line[4], line[5], line[6], line[11], dictionary)
					#наполняем unique
					doubled = 0
					for i in unique:
						if i['tag_id'] == line[3]:
							i['xNew'] = dictionary['x']
							i['yNew'] = dictionary['y']
							i['zNew'] = dictionary['z']
							i['time'] = dictionary['zone']
							i['zone_id'] = dictionary['zone_id']
							doubled = 1
					if not(doubled):
						unique.append(dictionary)
					# getUnique(line[3], float(line[4]), float(line[5]), float(line[6]), line[11], line[8])
		# включаем функцию корректировки по милисекундам
		if len(tumbler) == 0:
			tumbler.append(1)
			correctUniqueInMilisec()
		#send coordinates to usersession
		for i in active_users:
			try:
				if len(i['data']) > 0:
					service_queue('coords_lock', json({'user': i['id'],'data': i['data']}))
					i['data'] = []
			except:
				pass	
		return HttpResponse('ok')
	return HttpResponse('ok')

def testing(request):
	request.session.set_expiry(4000)
	line = "LabR,Std0,0000,00000a5,21.681625,55.457092,10.803710,7,2016-01-13T13:52:31:239+1,2,0038,0000"
	line = line.split(',')
	dictionary = {'tag_id':line[3], 'x': line[4], 'y': line[5], 'z': line[6], 'zone':line[8], 'zone_id': line[11]}
	x = getMarksByInterval(line[4], line[5], line[6], line[11], dictionary)
	return JsonResponse({'active_users': active_users})

def inInterval(i, imin, imax):
	if (i >= imin and i <= imax):
		return True
	else:
		return False

def getMarksByInterval(x, y, z, zone, dictionary):
	for i in active_users:
		try:
			if i['max']:
				xmax = i['max'].get('x')
				ymax = i['max'].get('y')
				zmax = i['max'].get('z')

				xmin = i['min'].get('x')
				ymin = i['min'].get('y')
				zmin = i['min'].get('z')

				landscape_id = i['landscape_id']
				if (inInterval(float(x), xmin, xmax) and inInterval(float(y), ymin, ymax) and inInterval(float(z), zmin, zmax) and zone ==landscape_id):
					i['data'].append(dictionary)
		except:
			pass

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

def values(request, landscape_id='0000'):
	args = {}
	landscape_id = landscape_id
	args['link'] = LoadLandscape.objects.get(landscape_id=landscape_id).landscape_source
	args['buildings'] = Building.objects.filter(LoadLandscape_id=landscape_id)
	args['floors'] = Floor.objects.filter(LoadLandscape_id=landscape_id)
	args['kabinet_n_outer'] = Kabinet_n_Outer.objects.filter(LoadLandscape_id=landscape_id)
	args['walls'] = Wall.objects.filter(LoadLandscape_id=landscape_id)
	args['username'] = auth.get_user(request).id
	args['landscape_id'] = landscape_id
	return render(request, 'values.html', args)

# def getmarksvalues(request):
# 	if request.method == 'POST':
# 		marks = {}
# 		line = massive['data']
# 		line = line.split('Zone')
# 		num = 0
# 		if (len(line) > 1):
# 			line = line[2]
# 			line = line.split(',')
# 			for i in line:
# 				spisok = []
# 				spisok.append({'tag_id':line[3], 'x': float(line[4]), 'y': float(line[5]), 'z': float(line[6]), 'zone':[8]})
# 				marks[num] = spisok
# 			return JsonResponse(marks)
# 		else:
# 			line = line[0].split('\n')
# 			for i in line:
# 				try:
# 					line = i.split(',')
# 					spisok = []
# 					spisok.append({'tag_id':line[3], 'x': float(line[4]), 'y': float(line[5]), 'z': float(line[6]), 'zone':line[8]})
# 					marks[num] = spisok
# 					num +=1
# 				except:
# 					pass
# 			return JsonResponse(marks)

# форма загрузки сцены
def landscapeloadform(request, result='error'):
	args = {}
	if result == 'load':
		if request.POST:
			landscape_name = request.POST['landscape_name']
			landscape_id = request.POST['landscape_id']
			landscape_source = request.FILES['landscape_file']
			try:
				obj = LoadLandscape.objects.get(landscape_id=landscape_id)
				LoadLandscape.objects.filter(landscape_id=landscape_id).update(landscape_name=landscape_name, landscape_id=landscape_id, landscape_source=landscape_source)
			except:
				data = LoadLandscape(landscape_name=landscape_name, landscape_id=landscape_id, landscape_source=landscape_source).save()
			return redirect('/landscapetreeload/%s' %landscape_id)
		return render(request, 'landscapeloadform.html', args)
	elif result == 'success':
		args['result'] = 'success'
		return render(request, 'landscapeloadform.html', args)

# запись элементов сцены в БД, установление связей
def landscapetreeload(request, landscape_id='0000', source=''):
	args = {}
	args['landscape_id'] = landscape_id
	args['source'] = LoadLandscape.objects.get(landscape_id=landscape_id).landscape_source
	return render(request, 'landscapetreeload.html', args)

def landscape_save(request):
	if request.method == 'POST':
		string = simplejson.loads(request.body)
		landscape = string['landscape'][0]
		landscape_id = string['landscape'][1]['name']

		Wall.objects.filter(LoadLandscape_id=landscape_id).delete()
		Kabinet_n_Outer.objects.filter(LoadLandscape_id=landscape_id).delete()
		Floor.objects.filter(LoadLandscape_id=landscape_id).delete()
		Building.objects.filter(LoadLandscape_id=landscape_id).delete()

		for i in landscape['object']['children']:
			if 'building' in i['name']:
				dae_BuildingName = i['name']
				landscape_id = landscape_id
				building = Building(dae_BuildingName=dae_BuildingName, LoadLandscape_id=landscape_id)
				building.save()
				for j in i['children']:
					if 'floor' in j['name']:
						dae_FloorName = j['name']
						floor = Floor(dae_FloorName=dae_FloorName, Building_id=building.id, LoadLandscape_id=landscape_id)
						floor.save()
						for x in j['children']:
							dae_Kabinet_n_OuterName = x['name']
							kabinet_n_outer = Kabinet_n_Outer(dae_Kabinet_n_OuterName=dae_Kabinet_n_OuterName, Floor_id=floor.id, LoadLandscape_id=landscape_id)
							kabinet_n_outer.save()
							if 'kabinet' in x['name']:
								for y in x['children']:
									dae_WallName = y['name']
									wall = Wall(dae_WallName=dae_WallName, Kabinet_n_Outer_id=kabinet_n_outer.id, LoadLandscape_id=landscape_id)
									wall.save()
		return JsonResponse({'name': landscape['object']['children']})

# sockjs manipulations
import redis
from django.conf import settings
try:
	from django.utils import simplejson
except:
	import simplejson


ORDERS_FREE_LOCK_TIME = getattr(settings, 'ORDERS_FREE_LOCK_TIME', 0)
ORDERS_REDIS_HOST = getattr(settings, 'ORDERS_REDIS_HOST', 'localhost')
ORDERS_REDIS_PORT = getattr(settings, 'ORDERS_REDIS_PORT', 6379)
ORDERS_REDIS_PASSWORD = getattr(settings, 'ORDERS_REDIS_PASSWORD', None)
ORDERS_REDIS_DB = getattr(settings, 'ORDERS_REDIS_DB', 0)

service_queue = redis.StrictRedis(
	host=ORDERS_REDIS_HOST,
	port=ORDERS_REDIS_PORT,
	db=ORDERS_REDIS_DB,
	password=ORDERS_REDIS_PASSWORD
).publish
json = simplejson.dumps

def sockjs(request):
	args = {}
	args['session'] = request.session.session_key
	args['username'] = auth.get_user(request).username
	args['id'] = auth.get_user(request).id
	request.session.set_expiry(4000)
	return render(request, 'sockjs.html', args)

def orderadd(request):
	a = Order(OrderName='neworder')
	a.save()
	service_queue('order_lock', json({'user': 1,'order': 10}))
	return JsonResponse({'result': 'ok'})

#create list of users
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone

def get_all_logged_in_users():
	sessions = Session.objects.filter(expire_date__gte = timezone.now())
	uid_list = []

	for session in sessions:
		data = session.get_decoded()
		uid_list.append(data.get('_auth_user_id', None))

	return User.objects.filter(id__in = uid_list)

def update_active_users():
	all_loged = get_all_logged_in_users()
	values = []
	for j in active_users:
		for i in all_loged:
			if j['id'] == i.id:
				values.append(i.id)

	for q in active_users:
		if not(q['id'] in values):
			active_users.remove(q)

	for i in all_loged:
		got = False
		for j in active_users:
			if j['id'] == i.id:
				got = True
		if not(got):
			active_users.append({'id': i.id})

# look sessions and their properties
def getsessions(request):
	update_active_users()
	return JsonResponse({'active_users':active_users, 'marks': marks})


def setproperty(request):
	for i in active_users:
		if i['id'] == 'ancel':
			i['property'] = 'property is set'
	return redirect('/sockjs')

# set min max to session
def minmaxtosession(request):
	if request.method == 'POST':
		update_active_users()
		unjson = simplejson.loads
		string = unjson(request.body)
		strmax = string['max']
		strmin = string['min']
		username = int(string['username'])
		landscape_id = string['landscape_id']
		for i in active_users:
			if i['id'] == username:
				i['max'] = strmax
				i['min'] = strmin
				i['landscape_id'] = landscape_id
				i['data'] = []
		return JsonResponse({'properties': active_users})

def sendcoordsform(request):
	return render(request, 'sendcoordsform.html')