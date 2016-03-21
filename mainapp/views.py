#!/usr/bin/python
# -*- coding: utf8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from mainapp.models import *
from django.db.models import Q
from django.contrib.auth.models import User
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
from shapely.geometry import *
import math

import pkg_resources
pkg_resources.require('matplotlib')
import pylab
import matplotlib.patches as patches

# глобальный словарь static статичные объекты
static = []
static_tumbler = []

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

# def getmarks(request):
# 	return HttpResponse(marks)

#static получить
def getstatic(request):
	return HttpResponse(static)
#переключить тумблер
def turnoff_tumbler(request):
	del static_tumbler[:]
	return HttpResponse('static_tumbler reseted')
#static очистить
def clearstatic(request):
	del static[:]
	return HttpResponse('static list cleared')

# наполняем статику
def fillStatic():
	landscape = LoadLandscape.objects.all()
	for l in landscape:
		static.append({'landscape_id': l.landscape_id, 'buildings': []})
		for i in static:
			if i['landscape_id'] == l.landscape_id:
				#building
				building = Building.objects.filter(LoadLandscape_id=l.landscape_id)
				bno = 0
				for b in building:
					i['buildings'].append({'id': b.id, 'name': b.dae_BuildingName, \
					 'floors':[], 'vertices': [], 'maxz': b.maxz, 'minz': b.minz, \
					 'IncomeZones': [], 'ExcludeZones': []})
					#add building vertices
					verticesBuilding = VerticesBuilding.objects.filter(Building_id=b.id)
					for v in verticesBuilding:
						i['buildings'][bno]['vertices'].append([float(v.x), float(v.y)])
					#сортировка вершин
					a = sortVert(i['buildings'][bno]['vertices'])
					i['buildings'][bno]['vertices'] = a
					# BuildingIncomeZone добавляем id зон
					biz = BuildingIncomeZone.objects.filter(Building_id=b.id)
					zno = 0
					for z in biz:
						i['buildings'][bno]['IncomeZones'].append({'id': z.IncomeZone_id, \
						 'vertices': [], 'minz': 0, 'maxz': 0})
						# BuildingIncomeZone добавляем вершины зон
						bizvert = VerticesIncomeZone.objects.filter(IncomeZone_id=z.IncomeZone_id)
						#минимальные и максимальные значения по высоте
						i['buildings'][bno]['IncomeZones'][zno]['minz'] = bizvert[0].zmin
						i['buildings'][bno]['IncomeZones'][zno]['maxz'] = bizvert[0].zmax
						for vert in bizvert:
							i['buildings'][bno]['IncomeZones'][zno]['vertices'].append( \
								[vert.xCoord, vert.yCoord])
						#сортировка вершин
						a = sortVert(i['buildings'][bno]['IncomeZones'][zno]['vertices'])
						i['buildings'][bno]['IncomeZones'][zno]['vertices'] = a
						zno += 1
					# BuildingExcludeZone добавляем id зон
					bez = BuildingExcludeZone.objects.filter(Building_id=b.id)
					zno = 0
					for z in bez:
						i['buildings'][bno]['ExcludeZones'].append({'id': z.ExcludeZone_id, \
							'vertices': [], 'minz': 0, 'maxz': 0})
						# BuildingExcludeZone добавляем вершины зон
						bezvert = VerticesExcludeZone.objects.filter(ExcludeZone_id=z.ExcludeZone_id)
						# минимальные и максимальные значения по высоте
						i['buildings'][bno]['ExcludeZones'][zno]['minz'] = bezvert[0].zmin
						i['buildings'][bno]['ExcludeZones'][zno]['maxz'] = bezvert[0].zmax
						for vert in bezvert:
							i['buildings'][bno]['ExcludeZones'][zno]['vertices'].append( \
								[vert.xCoord, vert.yCoord])
						#сортировка вершин
						a = sortVert(i['buildings'][bno]['ExcludeZones'][zno]['vertices'])
						i['buildings'][bno]['ExcludeZones'][zno]['vertices'] = a
						zno += 1
					#floor
					floor = Floor.objects.filter(Building_id=b.id)
					fno = 0
					for f in floor:
						i['buildings'][bno]['floors'].append({'id': f.id, \
						 'name': f.dae_FloorName, 'kabinets':[], \
						  'vertices': [], 'maxz': f.maxz, 'minz': f.minz, \
						  'IncomeZones': [], 'ExcludeZones': []})
						# добавляем вершины floor
						verticesFloor = VerticesFloor.objects.filter(Floor_id=f.id)
						for v in verticesFloor:
							i['buildings'][bno]['floors'][fno]['vertices'].append([float(v.x), float(v.y)])
						#сортировка вершин
						a = sortVert(i['buildings'][bno]['floors'][fno]['vertices'])
						i['buildings'][bno]['floors'][fno]['vertices'] = a
						# FloorIncomeZone добавляем id зон
						fiz = FloorIncomeZone.objects.filter(Floor_id=f.id)
						zno = 0
						for z in fiz:
							i['buildings'][bno]['floors'][fno]['IncomeZones'].append({ \
								'id': z.IncomeZone_id, 'vertices': [], 'minz': 0, 'maxz': 0})
							#FloorIncomeZone добавляем вершины зон
							fizvert = VerticesIncomeZone.objects.filter(IncomeZone_id=z.IncomeZone_id)
							#минимальные и максимальные значения по высоте
							i['buildings'][bno]['floors'][fno]['IncomeZones'][zno]['minz'] = \
							 fizvert[0].zmin
							i['buildings'][bno]['floors'][fno]['IncomeZones'][zno]['maxz'] = \
							 fizvert[0].zmax
							for vert in fizvert:
								i['buildings'][bno]['floors'][fno]['IncomeZones' \
								][zno]['vertices'].append([vert.xCoord, vert.yCoord])
							#сортировка вершин
							a = sortVert(i['buildings'][bno]['floors'][fno]['IncomeZones' \
								][zno]['vertices'])
							i['buildings'][bno]['floors'][fno]['IncomeZones'][zno]['vertices'] = a
							zno += 1
						# FloorExcludeZone добавляем id зон
						fez = FloorExcludeZone.objects.filter(Floor_id=f.id)
						zno = 0
						for z in fez:
							i['buildings'][bno]['floors'][fno]['ExcludeZones'].append({ \
								'id': z.ExcludeZone_id, 'vertices': [], 'minz': 0, 'maxz': 0})
							#FloorExcludeZone добавляем вершины зон
							fezvert = VerticesExcludeZone.objects.filter(ExcludeZone_id=z.ExcludeZone_id)
							#минимальные и максимальные значение по высоте
							i['buildings'][bno]['floors'][fno]['ExcludeZones'][zno]['minz'] = \
							 fezvert[0].zmin
							i['buildings'][bno]['floors'][fno]['ExcludeZones'][zno]['maxz'] = \
							 fezvert[0].zmax
							for vert in fezvert:
								i['buildings'][bno]['floors'][fno]['ExcludeZones' \
								][zno]['vertices'].append([vert.xCoord, vert.yCoord])
							# сортировка вершин
							a = sortVert(i['buildings'][bno]['floors'][fno]['ExcludeZones' \
								][zno]['vertices'])
							i['buildings'][bno]['floors'][fno]['ExcludeZones'][zno]['vertices'] = a
							zno += 1
						#kabinet
						kabinet  = Kabinet_n_Outer.objects.filter(Floor_id=f.id \
							).exclude(dae_Kabinet_n_OuterName__icontains='outer')
						kno = 0
						for k in kabinet:
							i['buildings'][bno]['floors'][fno]['kabinets']. \
							append({'id': k.id, 'name': k.dae_Kabinet_n_OuterName, 'vertices': [], \
							 'maxz': k.maxz, 'minz': k.minz, 'IncomeZones':[], 'ExcludeZones':[]})
							verticesKabinet_n_Outer = \
							 VerticesKabinet_n_Outer.objects.filter(Kabinet_n_Outer_id=k.id)
							for v in verticesKabinet_n_Outer:
								i['buildings'][bno]['floors'][fno]['kabinets'][kno]['vertices'].append([float(v.x), float(v.y)])
							#сортировка вершин
							a = sortVert(i['buildings'][bno]['floors'][fno]['kabinets'][kno]['vertices'])
							if a:
								i['buildings'][bno]['floors'][fno]['kabinets'][kno]['vertices'] = a
							# KabinetIncomeZone добавляем id зон
							kiz = KabinetIncomeZone.objects.filter(Kabinet_id=k.id)
							zno = 0
							for z in kiz:
								i['buildings'][bno]['floors'][fno]['kabinets'][kno]['IncomeZones'].append({ \
									'id': z.IncomeZone_id, 'vertices': [], 'minz': 0, 'maxz': 0})
								#KabinetIncomeZone добавляем вершины зон
								kizvert = VerticesIncomeZone.objects.filter(IncomeZone_id=z.IncomeZone_id)
								#минимальные и максимальные значения по высоте
								i['buildings'][bno]['floors'][fno]['kabinets'][kno]['IncomeZones'][zno]['minz'] = \
								 kizvert[0].zmin
							 	i['buildings'][bno]['floors'][fno]['kabinets'][kno]['IncomeZones'][zno]['maxz'] = \
							 	 kizvert[0].zmax
						 		for vert in kizvert:
						 			i['buildings'][bno]['floors'][fno]['kabinets'][kno]['IncomeZones'][zno]['vertices'].append([vert.xCoord, vert.yCoord])
								#сортировка вершин
								a = sortVert(i['buildings'][bno]['floors'][fno]['kabinets'][kno]['IncomeZones'][zno]['vertices'])
								i['buildings'][bno]['floors'][fno]['kabinets'][kno]['IncomeZones'][zno]['vertices'] = a
								zno += 1
							# KabinetExcludeZone добавляем id зон
							kez = KabinetExcludeZone.objects.filter(Kabinet_id=k.id)
							zno = 0
							for z in kez:
								i['buildings'][bno]['floors'][fno]['kabinets'][kno]['ExcludeZones'].append({ \
									'id': z.ExcludeZone_id, 'vertices': [], 'minz':0, 'maxz': 0})
								# KabinetExcludeZone добавляем вершины зон
								kezvert = VerticesExcludeZone.objects.filter(ExcludeZone_id=z.ExcludeZone_id)
								# минимальные и максимальные значения по высоте
								i['buildings'][bno]['floors'][fno]['kabinets'][kno]['ExcludeZones'][zno]['minz'] = \
								 kezvert[0].zmin
								i['buildings'][bno]['floors'][fno]['kabinets'][kno]['ExcludeZones'][zno]['maxz'] = \
								 kezvert[0].zmax
								for vert in kezvert:
									i['buildings'][bno]['floors'][fno]['kabinets'][kno]['ExcludeZones'][zno]['vertices'].append([vert.xCoord, vert.yCoord])
								#сортировка вершин
								a = sortVert(i['buildings'][bno]['floors'][fno]['kabinets'][kno]['ExcludeZones'][zno]['vertices'])
								i['buildings'][bno]['floors'][fno]['kabinets'][kno]['ExcludeZones'][zno]['vertices'] = a
								zno += 1
							kno += 1
						fno += 1
					bno += 1

#unique очистить
def clearUnique(request):
	del unique[:]
	return HttpResponse('unique dictionary cleared')
# получить unique
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
#быстрая unique корректировка
def correctFast(i):
	xCur = i['x']
	yCur = i['y']
	zCur = i['z']

	xNew = i['xNew']
	yNew = i['yNew']
	zNew = i['zNew']
	step = 0.3
	for j in unique:
		if j == i:
		    if (xCur < xNew + step) and ((xNew - xCur) > 0):
		        j['x'] += step
		    if (yCur < yNew + step) and ((yNew - yCur) > 0):
		        j['y'] += step
		    if (zCur < zNew + step) and ((zNew - zCur) > 0):
		        j['z'] += step
		    if (xCur > xNew + step) and ((xNew - xCur) < 0):
		        j['x'] -= step
		    if (yCur > yNew + step) and ((yNew - yCur) < 0):
		        j['y'] -= step
		    if (zCur > zNew + step) and ((zNew - zCur) < 0):
		        j['z'] -= step

#плавная unique корректировка
def correctF():
	for i in unique:
		if i['cron'] > 20:
			try:
				t = Tag.objects.get(TagId=i['tag_id'])
				TurnOnOffTag(OnOff=0, OnOffTime=datetime.datetime.now(), Tag_id=t.TagId).save()
				unique.remove(i)
			except:
				unique.remove(i)
	for i in unique:
		i['cron'] += 0.1

		xCur = i['x']
		yCur = i['y']
		zCur = i['z']

		xNew = i['xNew']
		yNew = i['yNew']
		zNew = i['zNew']

		step = 0.07
		if (xCur != xNew or yCur != yNew or zCur != zNew):
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
	#send coordinates to usersession
	for i in active_users:
		try:
			service_queue('coords_server_lock', json({'user': i['id'],'data': unique}))
		except:
			pass

# определение принадлежности метки объекту сцены
def UniqueToStatic():
	for i in unique:
		for s in static:
			if s['landscape_id'] ==  i['zone_id']:
				# создаем список подходящих зон входа
				findMatchingIncomeZones(i, i['zone_id'])
				# ищем подходящий кабинет
				findMatchingKabinet(i, i['zone_id'])

#ищем подходящий кабинет
def findMatchingKabinet(obj, landscape_id):
	# если отсутствует candidate
	# включаем хронометраж
	if not 'candidate' in obj or len(obj['candidate']) == 0:
		if not 'noLocation' in obj:
			obj['noLocation'] = {'cron': 0}
		else:
			obj['noLocation']['cron'] += 1
	elif len(obj['candidate']) > 0 and 'candidate' in obj:
		obj['noLocation']['cron'] = 0
	# увеличиваем cron
	if 'candidate' in obj:
		#удаляем просроченные candidate
		deleteFromListByKeyValueUpper(20, 'cron', obj['candidate'])
		#увеличиваем хронометраж
		for i in obj['candidate']:
			i['cron'] += 1
		#проверка есть ли candidate incomezone в списке incomezone если cron == 7,
		# и matchCount > 4
		for i in obj['candidate']:
			if i['cron'] == 7 and i['matchCount'] > 4:
				for caniz in i['IncomeZones']:
					candidateincomezone = caniz['id']
					for objiz in obj['IncomeZones']:
						if objiz['id'] == candidateincomezone:
							if 'location' in obj:
								if obj['location']['id'] != i['id']:
									obj['location']['id'] = i['id']
									obj['location']['type'] = 'kabinet'
									#очищаем Candidate и IncomeZones
									del obj['candidate'][:]
									del obj['IncomeZones'][:]
							else:
								obj['location'] = {'id': i['id'], 'type': 'kabinet'}
								#очищаем Candidate и IncomeZones
								del obj['candidate'][:]
								del obj['IncomeZones'][:]
		#проверка если candidate incomezone отсутствует в incomezone cron == 20, 
		# matchCount > 15
		for i in obj['candidate']:
			if i['cron'] == 20 and i['matchCount']>15:
				if 'location' in obj:
					if obj['location']['id'] != i['id']:
						obj['location']['id'] = i['id']
						obj['location']['type'] = 'kabinet'
						#очищаем Candidate и IncomeZones
						del obj['candidate'][:]
						del obj['IncomeZones'][:]
				else:
					obj['location'] = {'id': i['id'], 'type': 'kabinet'}
					#очищаем Candidate и IncomeZones
					del obj['candidate'][:]
					del obj['IncomeZones'][:]
	x = obj['x']
	y = obj['y']
	z = obj['z']
	for s in static:
		if s['landscape_id'] == landscape_id:
			for building in s['buildings']:
				for floor in building['floors']:
					# если нет candidates, noLocation > 20
					if obj['noLocation']['cron'] > 20:
						minz = floor['minz']
						maxz = floor['maxz']
						vertices = floor['vertices']
						vector = [(x, y)]
						match = inPolygon(vertices, vector)
						if (match and inInterval(z, minz, maxz)):
							inZone = 0
							for ez in floor['ExcludeZones']:
								vertices = ez['vertices']
								minz = ez['minz']
								maxz = ez['maxz']
								match = inPolygon(vertices, vector)
								if (match and inInterval(z, minz, maxz)):
									inZone = 1
							if not inZone:
								obj['location'] = {'id': floor['id'], 'type': 'floor'}
								obj['noLocation']['cron'] = 0
					for kabinet in floor['kabinets']:
						vertices = kabinet['vertices']
						vector = [(x, y)]
						minz = kabinet['minz']
						maxz = kabinet['maxz']
						match = inPolygon(vertices, vector)
						if (match and inInterval(z, minz, maxz)):
							# проверяем входит ли в зону исключения
							inZone = 0
							for ez in kabinet['ExcludeZones']:
								vertices = ez['vertices']
								minz = ez['minz']
								maxz = ez['maxz']
								match = inPolygon(vertices, vector)
								if (match and inInterval(z, minz, maxz)):
									inZone = 1
							if not inZone:
							 	if not 'candidate' in obj:
							 		obj['candidate'] = []
						 		elif not(dictKeyInArray(kabinet['id'], 'id', obj['candidate'], 0)):
									obj['candidate'].append({'id': kabinet['id'], 'cron': 0, \
										'matchCount': 0, 'IncomeZones': kabinet['IncomeZones']})
								#если есть кандидат, зафиксировать попадание в matchCount
								else:
									updateMatchCount(kabinet['id'], 'id', obj['candidate'])

# отметить попадание MatchCount
def updateMatchCount (value, dictKey, arr):
	for i in arr:
		if i[dictKey] == value:
			i['matchCount'] += 1
			return False

# cоздаем список подходящих зона входа
def findMatchingIncomeZones(obj, landscape_id):
	x = obj['x']
	y = obj['y']
	z = obj['z']
	matchingzones = []
	#проверка наличия ключа
	if not 'IncomeZones' in obj:
		obj['IncomeZones'] = []
	else:
		#удаляем просроченные IncomeZones
		deleteFromListByKeyValueUpper(5, 'cron', obj['IncomeZones'])
	for s in static:
		if s['landscape_id'] == landscape_id:
			# заполняем зоны входа buildings
			for building in s['buildings']:
				for biz in building['IncomeZones']:
					vertices = biz['vertices']
					vector = [(x, y)]
					minz = biz['minz']
					maxz = biz['maxz']
					match = inPolygon(vertices, vector)
					if (match and inInterval(z, minz, maxz)):
						# проверяем наличие id building в IncomeZones
						if not dictKeyInArray(biz['id'], 'id', obj['IncomeZones'], 0):
							# записываем id в словарь
							obj['IncomeZones'].append({'id': biz['id'], 'cron': 0})
						else:
							dictKeyInArray(biz['id'], 'id', obj['IncomeZones'], 1)
				# заполняем зоны входа floors
				for floor in building['floors']:
					for fiz in floor['IncomeZones']:
						vertices = fiz['vertices']
						vector = [(x, y)]
						minz = fiz['minz']
						maxz = fiz['maxz']
						match = inPolygon(vertices, vector)
						if (match and inInterval(z, minz, maxz)):
							# проверяем наличие id floor в IncomeZones
							if not dictKeyInArray(fiz['id'], 'id', obj['IncomeZones'], 0):
								# записываем id в словарь
								obj['IncomeZones'].append({'id': fiz['id'], 'cron': 0})
							else:
								dictKeyInArray(fiz['id'], 'id', obj['IncomeZones'], 1)
					# заполняем зоны входа kabinets
					for kabinet in floor['kabinets']:
						for kiz in kabinet['IncomeZones']:
							vertices = kiz['vertices']
							vector = [(x, y)]
							minz = kiz['minz']
							maxz = kiz['maxz']
							match = inPolygon(vertices, vector)
							if (match and inInterval(z, minz, maxz)):
								# проверяем наличие id kabinet в IncomeZones
								if not dictKeyInArray(kiz['id'], 'id', obj['IncomeZones'], 0):
									# записываем id в словарь
									obj['IncomeZones'].append({'id': kiz['id'], 'cron': 0})
								else:
									dictKeyInArray(kiz['id'], 'id', obj['IncomeZones'], 1)

# функци проверки значения в списке по ключу
# (если cron, appendCron = 1, в других случаях 0)
def dictKeyInArray(value, dictKey, arr, appendCron):
	for i in arr:
		if i[dictKey] == value:
			if appendCron:
				i['cron'] += 1
			return True
	return False
# удалени из списка по значению ключа
def deleteFromListByKeyValueUpper(value, key, arr):
	for i in arr:
		if i[key] > value:
			arr.remove(i)
# найти подходящий под вектор объект, типы искомых объектов в obj_type
def findMatchingStatic(obj, landscape_id, obj_type):
	x = obj['x']
	y = obj['y']
	z = obj['z']
	for s in static:
		if s['landscape_id'] == landscape_id:
			for elem in s['objects']:
				if obj_type in elem['name']:
					obj_typeVertices = elem['vertices']
					uniqueVector = [(float(x), float(y))]
					minz = elem['minz']
					maxz = elem['maxz']
					match = inPolygon(obj_typeVertices, uniqueVector)
					if (match and inInterval(float(z), minz, maxz)):
						return elem['name']

# функция сервера с шагом
def correctUniqueInMilisec():
	if tumbler[0]:
		set_interval(correctF, 0.1)
		set_interval(UniqueToStatic, 1)

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
				if len(line) > 0 and len(line) > 4:
					dictionary = {'tag_id':line[3], 'x': float(line[4]), 'y': float(line[5]), 'z': float(line[6]), 'zone':line[8], 'zone_id': line[11]}
					getMarksByInterval(line[4], line[5], line[6], line[11], dictionary)
					#наполняем unique
					doubled = 0
					for i in unique:
						if i['tag_id'] == line[3]:
							i['xNew'] = float(dictionary['x'])
							i['yNew'] = float(dictionary['y'])
							i['zNew'] = float(dictionary['z'])
							i['time'] = dictionary['zone']
							i['zone_id'] = dictionary['zone_id']
							i['cron'] = 0
							#быстрая корректировка
							correctFast(i)
							doubled = 1
					if not(doubled):
						try:
							t = Tag.objects.get(TagId=dictionary['tag_id'])
							TurnOnOffTag(Tag_id=t.TagId, OnOff=1, OnOffTime=datetime.datetime.now()).save()
						except:
							pass
						unique.append(dictionary)
		# включаем функцию корректировки по милисекундам
		if len(tumbler) == 0:
			tumbler.append(1)
			correctUniqueInMilisec()
		# static включаем фунцию наполнения
		if len(static_tumbler) == 0:
			static_tumbler.append(1)
			fillStatic()
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
	if (float(i) >= float(imin) and float(i) <= float(imax)):
		return True
	else:
		return False

def inPolygon(vertices, vector):
	poly = Polygon(vertices)
	point = MultiPoint(vector).convex_hull
	return point.within(poly)

def getMarksByInterval(x, y, z, zone, dictionary):
	for i in active_users:
		try:
			if i['max']:
				xmax = i['max'].get('x')
				xmin = i['min'].get('x')

				ymax = i['max'].get('y')
				ymin = i['min'].get('y')

				zmax = i['max'].get('z')
				zmin = i['min'].get('z')

				landscape_id = i['landscape_id']
				if len(i['vertices']) > 0:
					match = inPolygon(i['vertices'], [(float(x), float(y))])
					if (match and inInterval(z, zmin, zmax) and zone ==landscape_id):
						i['data'].append(dictionary)
		except:
			pass

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

# look to smooth node movement
def values_server(request, landscape_id='0000'):
	args = {}
	landscape_id = landscape_id
	args['sceneop'] = LoadLandscape.objects.get(landscape_id=landscape_id)
	args['link'] = LoadLandscape.objects.get(landscape_id=landscape_id).landscape_source
	args['lcolor'] = LandscapeColor.objects.all()
	args['buildings'] = Building.objects.filter(LoadLandscape_id=landscape_id)
	args['bcolor'] = BuildingColor.objects.all()
	args['floors'] = Floor.objects.filter(LoadLandscape_id=landscape_id)
	args['fcolor'] = FloorColor.objects.all()
	args['kabinet_n_outer'] = Kabinet_n_Outer.objects.filter(LoadLandscape_id=landscape_id)
	args['kcolor'] = KabinetColor.objects.all()
	args['walls'] = Wall.objects.filter(LoadLandscape_id=landscape_id)
	args['username'] = auth.get_user(request).id
	args['landscape_id'] = landscape_id
	args['tags'] = Tag.objects.all()
	args['taggroup'] = TagGroup_Tag.objects.filter(User_id=auth.get_user(request).id).values( \
		'Tag_id', 'User_id', 'TagGroup__GroupName', 'TagGroup__MeshGeometry', 'TagGroup__MeshColor', \
		'TagGroup__CircleColor')
	return render(request, 'values_server.html', args)

def values(request, landscape_id='0000'):
	args = {}
	landscape_id = landscape_id
	args['sceneop'] = LoadLandscape.objects.get(landscape_id=landscape_id)
	args['link'] = LoadLandscape.objects.get(landscape_id=landscape_id).landscape_source
	args['lcolor'] = LandscapeColor.objects.all()
	args['buildings'] = Building.objects.filter(LoadLandscape_id=landscape_id)
	args['bcolor'] = BuildingColor.objects.all()
	args['floors'] = Floor.objects.filter(LoadLandscape_id=landscape_id)
	args['fcolor'] = FloorColor.objects.all()
	args['kabinet_n_outer'] = Kabinet_n_Outer.objects.filter(LoadLandscape_id=landscape_id)
	args['kcolor'] = KabinetColor.objects.all()
	args['walls'] = Wall.objects.filter(LoadLandscape_id=landscape_id)
	args['username'] = auth.get_user(request).id
	args['landscape_id'] = landscape_id
	args['tags'] = Tag.objects.all()
	args['taggroup'] = TagGroup_Tag.objects.filter(User_id=auth.get_user(request).id).values( \
		'Tag_id', 'User_id', 'TagGroup__GroupName', 'TagGroup__MeshGeometry', 'TagGroup__MeshColor', \
		'TagGroup__CircleColor')
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
			l_id = request.POST['landscape_id']
			landscape_source = request.FILES['landscape_file']
			try:
				obj = LoadLandscape.objects.get(landscape_id=landscape_id)
				LoadLandscape.objects.filter(landscape_id=landscape_id).update(landscape_name=landscape_name, landscape_id=landscape_id, landscape_source=landscape_source)
			except:
				data = LoadLandscape(landscape_name=landscape_name, landscape_id=l_id, landscape_source=landscape_source, circle_step_symbol=0, get_wall_height_symbol=0, light_target_symbol=0).save()
			return redirect('/landscapetreeload/%s' %l_id)
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
		landscape = string['colladaObjects']['landscape'][0]
		landscape_id = string['landscape_id']
		vertices = string['verticesDict']
		# записываем SceneOptions параметры в таблицу LoadLandscape
		sceneoptions = string['sceneOptions'] 
		p = LoadLandscape.objects.get(landscape_id=landscape_id)
		p.camera_position_x = string['sceneOptions']['CameraPosition']['x']
		p.camera_position_y = string['sceneOptions']['CameraPosition']['y']
		p.camera_position_z = string['sceneOptions']['CameraPosition']['z']
		p.camera_up_x = string['sceneOptions']['CameraUp']['x']
		p.camera_up_y = string['sceneOptions']['CameraUp']['y']
		p.camera_up_z = string['sceneOptions']['CameraUp']['z']
		p.controls_target_x = string['sceneOptions']['ControlsTarget']['x']
		p.controls_target_y = string['sceneOptions']['ControlsTarget']['y']
		p.controls_target_z = string['sceneOptions']['ControlsTarget']['z']
		p.dae_rotation_x = string['sceneOptions']['DaeRotation']['x']
		p.dae_rotation_y = string['sceneOptions']['DaeRotation']['y']
		p.dae_rotation_z = string['sceneOptions']['DaeRotation']['z']
		p.dae_position_x = string['sceneOptions']['DaePosition']['x']
		p.dae_position_y = string['sceneOptions']['DaePosition']['y']
		p.dae_position_z = string['sceneOptions']['DaePosition']['z']
		p.circle_step_symbol = string['sceneOptions']['CircleStepSymbol']
		p.get_wall_height_symbol = string['sceneOptions']['GetWallHeightSymbol']
		p.light_target_symbol = string['sceneOptions']['LightTargetSymbol']
		p.save()

		Wall.objects.filter(LoadLandscape_id=landscape_id).delete()
		Kabinet_n_Outer.objects.filter(LoadLandscape_id=landscape_id).delete()
		Floor.objects.filter(LoadLandscape_id=landscape_id).delete()
		Building.objects.filter(LoadLandscape_id=landscape_id).delete()
		VerticesBuilding.objects.filter(LoadLandscape_id=landscape_id).delete()
		VerticesFloor.objects.filter(LoadLandscape_id=landscape_id).delete()
		VerticesKabinet_n_Outer.objects.filter(LoadLandscape_id=landscape_id).delete()

		for i in landscape['object']['children']:
			if 'building' in i['name']:
				dae_BuildingName = i['name']
				landscape_id = landscape_id
				#наполняем BoxMin, BoxMax
				for v in vertices['element']:
					if v['name'] == dae_BuildingName:
						maxx = v['BoxMax']['x']
						maxy = v['BoxMax']['y']
						maxz = v['BoxMax']['z']

						minx = v['BoxMin']['x']
						miny = v['BoxMin']['y']
						minz = v['BoxMin']['z']
				building = Building(dae_BuildingName=dae_BuildingName, LoadLandscape_id=landscape_id, maxx=maxx, maxy=maxy, maxz=maxz, minx=minx, miny=miny, minz=minz)
				building.save()
				#наполняем вершины building
				for v in vertices['element']:
					if v['name'] == dae_BuildingName:
						for vert in v['vertices']:
							VerticesBuilding(x=vert['x'], y=vert['y'], Building_id=building.id, LoadLandscape_id=landscape_id).save()
				for j in i['children']:
					if 'floor' in j['name']:
						dae_FloorName = j['name']
						#наполняем BoxMin, BoxMax
						for v in vertices['element']:
							if v['name'] == dae_FloorName:
								maxx = v['BoxMax']['x']
								maxy = v['BoxMax']['y']
								maxz = v['BoxMax']['z']

								minx = v['BoxMin']['x']
								miny = v['BoxMin']['y']
								minz = v['BoxMin']['z']
						floor = Floor(dae_FloorName=dae_FloorName, Building_id=building.id, LoadLandscape_id=landscape_id, maxx=maxx, maxy=maxy, maxz=maxz, minx=minx, miny=miny, minz=minz)
						floor.save()
						# наполняем вершины floor
						for v in vertices['element']:
							if v['name'] == dae_FloorName:
								for vert in v['vertices']:
									VerticesFloor(x=vert['x'], y=vert['y'], Floor_id=floor.id, LoadLandscape_id=landscape_id).save()
						for x in j['children']:
							dae_Kabinet_n_OuterName = x['name']
							# наполняем BoxMin, BoxMax
							for v in vertices['element']:
								if v['name'] == dae_Kabinet_n_OuterName:
									maxx = v['BoxMax']['x']
									maxy = v['BoxMax']['y']
									maxz = v['BoxMax']['z']

									minx = v['BoxMin']['x']
									miny = v['BoxMin']['y']
									minz = v['BoxMin']['z']
							kabinet_n_outer = Kabinet_n_Outer(dae_Kabinet_n_OuterName=dae_Kabinet_n_OuterName, Floor_id=floor.id, LoadLandscape_id=landscape_id, maxx=maxx, maxy=maxy, maxz=maxz, minx=minx, miny=miny, minz=minz)
							kabinet_n_outer.save()
							# наполняем вершины kabinet
							for v in vertices['element']:
								if v['name'] == dae_Kabinet_n_OuterName:
									for vert in v['vertices']:
										VerticesKabinet_n_Outer(x=vert['x'], y=vert['y'], Kabinet_n_Outer_id=kabinet_n_outer.id, LoadLandscape_id=landscape_id).save()
							if 'kabinet' in x['name']:
								try:
									for y in x['children']:
										dae_WallName = y['name']
										wall = Wall(dae_WallName=dae_WallName, Kabinet_n_Outer_id=kabinet_n_outer.id, LoadLandscape_id=landscape_id)
										wall.save()
								except:
									pass
		return JsonResponse({'string': string})

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
		dae_elem = string['dae_elem']
		username = int(string['username'])
		landscape_id = string['landscape_id']
		for i in active_users:
			if i['id'] == username:
				i['max'] = strmax
				i['min'] = strmin
				i['landscape_id'] = landscape_id
				i['dae_elem'] = dae_elem
				i['data'] = []
				i['vertices'] = []
				# наполняем вершинами x, y
				for s in static:
					if s['landscape_id'] == landscape_id:
						i['vertices'] = lookUpElemInStatic(dae_elem, s['buildings'])
		return JsonResponse({'properties': active_users})

def lookUpElemInStatic(name, arr):
	for b in arr:
		if b['name'] == name:
			return b['vertices']
		for f in b['floors']:
			if f['name'] == name:
				return f['vertices']
			for k in  f['kabinets']:
				if k['name'] == name:
					return k['vertices']

def sendcoordsform(request):
	return render(request, 'sendcoordsform.html')

# reports
def simplereport(request, parameters=0):
	if request.POST:
		args = {}
		args['error'] = []
		if parameters == '1':
			if request.POST['unique']:
				unique = request.POST['unique']
				tag = Tag.objects.filter(TagId=unique)
				if len(tag) == 0:
					args['error'].append({'incorrect_id': True})
				else:
					BldChange.objects.filter(Tag_id=unique).delete()
					FlrChange.objects.filter(Tag_id=unique).delete()
					KbntChange.objects.filter(Tag_id=unique).delete()
				return redirect('/simplereport/0')
		if request.POST['unique']:
			unique = request.POST['unique']
			args['unique'] = unique
			tag = Tag.objects.filter(TagId=unique)
			if len(tag) == 0:
				args['error'].append({'incorrect_id': True})
			else:
				# строения
				bldchange = BldChange.objects.filter(Tag_id=unique). \
				values('Tag__TagType', 'Tag__Name', 'ChangeTime', \
				 'BldNew__dae_BuildingName', 'BldNew__BuildingName').order_by('-ChangeTime')
				args['bldchange'] = bldchange
				# этажи
				flrchange = FlrChange.objects.filter(Tag_id=unique). \
				values('Tag__TagType', 'Tag__Name', 'ChangeTime', \
				 'FlrNew__dae_FloorName', 'FlrNew__FloorName').order_by('-ChangeTime')
				args['flrchange'] = flrchange
				# кабинеты
				kbntchange = KbntChange.objects.filter(Tag_id=unique). \
				values('Tag__TagType', 'Tag__Name', 'ChangeTime', \
				 'KbntNew__dae_Kabinet_n_OuterName', 'KbntNew__Kabinet_n_OuterName').order_by('-ChangeTime')
				args['kbntchange'] = kbntchange
		else:
			args['error'].append({'empty_unique': True})
		return render(request, 'simplereport.html', args)
	return render(request, 'simplereport.html')
# Нормальная матрица
# def matrix(request):
# 	m = [-0.00018728063150774688, \
# 	-0.00006872335507068783, \
# 	-0.000014250318599806633, \
# 	-0.00007018526957836002, \
# 	0.00018337969959247857, \
# 	0.000038025180401746184, \
# 	6.856382572806297e-9, \
# 	0.2030385285615921, \
# 	-0.9791707396507263
# 	]
# 	return HttpResponse(getAngleAxis(m))


# def getAngleAxis(m):
#     xx = m[0]
#     yy = m[4]
#     zz = m[8]
 
#     # Сумма элементов главной диагонали
#     traceR = xx + yy + zz
 
#     # Угол поворота
#     theta = math.acos((traceR - 1) * 0.5)
 
#     # Упростим вычисление каждого элемента вектора
#     omegaPreCalc = 1.0 / (2 * math.sin(theta))
 
#     # Вычисляем вектор
#     w = {}
#     w['x'] = omegaPreCalc * (m[7] - m[5])
#     w['y'] = omegaPreCalc * (m[2] - m[6])
#     w['z'] = omegaPreCalc * (m[3] - m[1])
 
#     # Получаем угол поворота и ось, 
#     # относительно которой был поворот
#     return (theta*(180/math.pi), w)


def match(request):
	# obj_typeVertices = [[10.2411702602139, 77.2020180078125], [40.0918277492793, 77.2020180078125], [10.2411702602139, 37.2824776785943], [22.2700845101335, 29.1969969911337], [22.313131222691, 32.2875236674882], [17.9645475438023, 37.2824776785943], [40.0918277492793, 32.1710069062937], [32.1380708538545, 29.1969969911337], [32.1251458030088, 32.3618649137633]]
	# false
	# uniqueVector = [(28.49, 56.51)]
	# true
	# uniqueVector = [(25.49, 58.49)]
	pp = [[10.2411702602139, 77.2020180078125], [40.0918277492793, 77.2020180078125], [10.2411702602139, 37.2824776785943], [22.2700845101335, 29.1969969911337], [22.313131222691, 32.2875236674882], [17.9645475438023, 37.2824776785943], [40.0918277492793, 32.1710069062937], [32.1380708538545, 29.1969969911337], [32.1251458030088, 32.3618649137633]]
	#compute centroid
	cent  = (sum([p[0] for p in pp])/len(pp), sum([p[1] for p in pp])/len(pp))
	#sort by polar angle
	pp.sort(key=lambda p: math.atan2(p[1]-cent[1], p[0]-cent[0]))
	match = inPolygon(pp, [(25.49, 58.49)])
	return HttpResponse(match)

def getactiveusers(request):
	return HttpResponse(active_users)

# Имя, цвет каждому объекту сцены
def definemain(request, parameters=9999):
	args = {}
	args['username'] = auth.get_user(request).id
	args['parameters'] = parameters
	args['landscape'] = LoadLandscape.objects.all()
	args['lcolor'] = LandscapeColor.objects.all()
	if parameters == '9999':
		parameters = '0000'
	args['buildings'] = Building.objects.filter(LoadLandscape_id=parameters)
	args['bcolor'] = BuildingColor.objects.all()
	args['floors'] = Floor.objects.filter(LoadLandscape_id=parameters)
	args['fcolor'] = FloorColor.objects.all()
	args['kabinets'] = Kabinet_n_Outer.objects.filter(LoadLandscape_id=parameters \
		).exclude(dae_Kabinet_n_OuterName__icontains='outer')
	args['kcolor'] = KabinetColor.objects.all()
	if request.method == 'POST':
		string = simplejson.loads(request.body)
		#сохраняем наименование
		if (len(string['landscape']['name']) > 0): 
			LoadLandscape.objects.filter(landscape_id=string['landscape']['id']).update(landscape_name=string['landscape']['name'])
		#записываем цвет
		try:
			a = LandscapeColor.objects.get(User_id=string['user'], \
			 LoadLandscape_id=string['landscape']['id'])
			LandscapeColor.objects.filter(User_id=string['user'], \
			 LoadLandscape_id=string['landscape']['id']).update(lcolor=string['landscape']['color'])
		except LandscapeColor.DoesNotExist:
			LandscapeColor(User_id=string['user'], LoadLandscape_id=string['landscape']['id'], \
				lcolor=string['landscape']['color']).save()
		for b in string['building']:
			#сохраняем наименование
			if (len(b['name']) > 0):
				Building.objects.filter(id=b['id']).update(BuildingName=b['name'])
			#записываем цвет
			try:
				building = BuildingColor.objects.get(User_id=string['user'], \
					Building_id=b['id'])
				BuildingColor.objects.filter(User_id=string['user'], \
					Building_id=b['id']).update(bcolor=b['color'])
			except BuildingColor.DoesNotExist:
				BuildingColor(User_id=string['user'], Building_id=b['id'], bcolor=b['color']).save()
		for f in string['floor']:
			# сохраняем наименование
			if (len(f['name']) > 0):
				Floor.objects.filter(id=f['id']).update(FloorName=f['name'])
			# записываем цвет
			try:
				floor = FloorColor.objects.get(User_id=string['user'], \
					Floor_id=f['id'])
				FloorColor.objects.filter(User_id=string['user'], \
					Floor_id=f['id']).update(fcolor=f['color'])
			except FloorColor.DoesNotExist:
				FloorColor(User_id=string['user'], Floor_id=f['id'], fcolor=f['color']).save()
		for k in string['kabinet']:
			# сохраняем наименование
			if (len(k['name']) > 0):
				Kabinet_n_Outer.objects.filter(id=k['id']).update(Kabinet_n_OuterName=k['name'])
			# записываем цвет
			try:
				kabinet = KabinetColor.objects.get(User_id=string['user'], \
					Kabinet_id=k['id'])
				KabinetColor.objects.filter(User_id=string['user'], \
					Kabinet_id=k['id']).update(kcolor = k['color'])
			except KabinetColor.DoesNotExist:
				KabinetColor(User_id=string['user'], Kabinet_id=k['id'], kcolor=k['color']).save()
		return JsonResponse({'string': string})
	return render(request, 'definemain.html', args)

# TagGroup define module
def definetaggroup(request, parameters=1, geomtype='sphere'):
	args = {}
	args['error'] = []
	if request.method=='POST':
		string = simplejson.loads(request.body)
		for i in string['geometry']['parameters']:
			if not (i['value'] > 0):
				args['error'].append({'name': i['name'], 'type':'empty_input', 'ru': 'пустое поле'})
		if len(args['error']) > 0:
			# возвращаем ошибки
			return JsonResponse({'error': args['error']})
		else:
			#пишем
			user = User.objects.get(id=auth.get_user(request).id)
			TagGroup.objects.filter(User_id=user.id, id=string['groupid']).update( \
				GroupName=string['groupname'], MeshGeometry=string['geometry'], \
				MeshColor=string['meshcolor'], CircleColor=string['circlecolor'], \
				User_id=user.id)
			return JsonResponse({'string': string});
	args['username'] = auth.get_user(request).id
	args['parameters'] = int(parameters)
	args['geomtype'] = geomtype
	args['groups'] = TagGroup.objects.all()
	args['geometry'] = [{'type': 'sphere', 'ru': 'сфера', 'parameters': \
	 [{'name': 'radius', 'ru': 'радиус'}, {'name': 'widthsegments', 'ru': 'сегментов по ширине'}, \
	  {'name': 'heigthsegments', 'ru': 'сегментов по высоте'} ]}, \
	  {'type': 'box', 'ru': 'куб', 'parameters': \
	   [{'name':'width', 'ru': 'ширина'}, {'name': 'heigth' , 'ru': 'высота'}, \
	    {'name':'depth', 'ru': 'глубина'}]}, \
	  {'type': 'torus', 'ru': 'кольцо', 'parameters': [{'name':'radius', 'ru':'радиус'}, \
	   {'name': 'tube', 'ru': 'ширина'}, {'name':'radialsegments', 'ru': 'боковых сегментов'}, \
	   {'name': 'tubularsegments', 'ru': 'продольных сегментов'}]}, \
	   {'type': 'cylinder', 'ru': 'цилиндр', 'parameters': \
	    [{'name':'radiustop', 'ru': 'радиус верхней части'}, \
	    {'name': 'radiusbottom', 'ru': 'радиус нижней части'}, \
	     {'name': 'heigth', 'ru': 'высота'}, {'name': 'radiussegments', 'ru': 'количество ребер'}]}
	  ]
	return render(request, 'definetaggroup.html', args)

def taggroupmanager(request, user=1):
	args = {}
	args['username'] = auth.get_user(request).id
	args['username_name'] = User.objects.get(id=args['username'])
	args['groups'] = TagGroup.objects.filter(User_id=args['username'])
	meshtype = []
	for group in args['groups']:
		meshtype.append({'id': group.id, 'type': group.MeshGeometry['type']})
	args['meshtype'] = meshtype
	if request.method == "POST":
		string = simplejson.loads(request.body)
		if string['action'] == 'add':
			TagGroup(GroupName='Новая группа', User_id=auth.get_user(request).id, \
			 MeshGeometry={'type':'box', 'parameters':[{'name': 'width', 'value': 0.3}, \
			 {'name': 'heigth' , 'value':0.3}, {'name': 'depth', 'value':0.3}]}).save()
			return JsonResponse({'ok': 'ok'})
		if string['action'] == 'delete':
			groupid = string['id']
			TagGroup(id=groupid).delete()
			return JsonResponse({'ok': 'ok'})
	return render(request, 'taggroupmanager.html', args)

def taginoutgroup(request, group=1):
	args = {}
	args['username'] = auth.get_user(request).id
	args['username_name'] = User.objects.get(id=args['username'])
	args['groupid'] = group
	args['group'] = TagGroup.objects.get(User_id=auth.get_user(request).id, id=group)
	args['tag'] = Tag.objects.all()
	args['tagothergroup'] = TagGroup_Tag.objects.filter(User_id= \
		auth.get_user(request).id).exclude(TagGroup_id=group).values('Tag_id', \
		 'TagGroup__GroupName', 'TagGroup_id')
	args['taggroup_tag'] = TagGroup_Tag.objects.filter(TagGroup_id=group, \
	 User_id=auth.get_user(request).id).values('Tag__TagId', 'Tag__TagType', 'Tag__Name')
	unregistred = []
	for i in unique:
		getinunique = 0
		for t in args['tag']:
			if i['tag_id'] == t.TagId:
				getinunique = 1
		if getinunique == 0:
			unregistred.append(i)
	args['unregistred'] = unregistred
	if request.method == "POST":
		string = simplejson.loads(request.body)
		tagid = string['tagid']
		groupid = string['groupid']
		action = string['action']
		if (action == 'link' and len(TagGroup_Tag.objects.filter(Tag_id=tagid, \
		 TagGroup_id=groupid, User_id=auth.get_user(request).id)) == 0):
			TagGroup_Tag(Tag_id=tagid, TagGroup_id=groupid, User_id=auth.get_user(request).id \
				).save()
		if (action == 'unlink'):
			TagGroup_Tag.objects.filter(Tag_id=tagid, TagGroup_id=groupid, User_id=auth.get_user(request).id).delete()
		return JsonResponse({'ok': 'ok'})
	return render(request, 'taginoutgroup.html', args)

def tagregister(request, tag_id=0):
	args = {}
	args['error'] = []
	args['tag_id'] = tag_id
	args['username'] = auth.get_user(request).id
	args['tagtype'] = TagType.objects.all()
	try:
		args['tag'] = Tag.objects.get(TagId=tag_id)
	except:
		pass
	if request.method == "POST":
		tType = request.POST['TagType']
		Name = request.POST['Name']
		if not(Name):
			args['error'].append({'name': 'Отсутствует имя'})
		if not(tType):
			args['error'].append({'type': 'Отстутствует тип метки'})
		if (len(args['error']) == 0) :
			Tag(TagId=tag_id, TagType_id=tType, Name=Name).save()
			args['tag'] = Tag.objects.get(TagId=tag_id)
			args['success'] = 'Информация успешно внесена'
	return render(request, 'tagregister.html', args)

# incomezone
def incomezonedefine(request, landscape_id='0000'):
	args = {}
	landscape_id = landscape_id
	args['sceneop'] = LoadLandscape.objects.get(landscape_id=landscape_id)
	args['link'] = LoadLandscape.objects.get(landscape_id=landscape_id).landscape_source
	args['lcolor'] = LandscapeColor.objects.all()
	args['buildings'] = Building.objects.filter(LoadLandscape_id=landscape_id)
	args['bcolor'] = BuildingColor.objects.all()
	args['floors'] = Floor.objects.filter(LoadLandscape_id=landscape_id)
	args['fcolor'] = FloorColor.objects.all()
	args['kabinet_n_outer'] = Kabinet_n_Outer.objects.filter(LoadLandscape_id=landscape_id \
		).exclude(dae_Kabinet_n_OuterName__icontains='outer')
	args['kcolor'] = KabinetColor.objects.all()
	args['walls'] = Wall.objects.filter(LoadLandscape_id=landscape_id)
	args['username'] = auth.get_user(request).id
	args['landscape_id'] = landscape_id
	args['zones'] = IncomeZone.objects.filter(LoadLandscape_id=landscape_id)
	args['ezones'] = ExcludeZone.objects.filter(LoadLandscape_id=landscape_id)
	args['vzones'] = VerticesIncomeZone.objects.all()
	args['evzones'] = VerticesExcludeZone.objects.all()
	args['bIncomeZone'] = BuildingIncomeZone.objects.all()
	args['bExcludeZone'] =  BuildingExcludeZone.objects.all()
	args['fIncomeZone'] = FloorIncomeZone.objects.all()
	args['fExcludeZone'] = FloorExcludeZone.objects.all()
	args['kIncomeZone'] = KabinetIncomeZone.objects.all()
	args['kExcludeZone'] = KabinetExcludeZone.objects.all()
	if request.method == 'POST':
		string = simplejson.loads(request.body)
		landscape_id = string['landscape_id']
		#добавить зону входа
		if string['method'] == 'add':
			zone = IncomeZone.objects.create(LoadLandscape_id=landscape_id)
			zoneId = zone.id
			for i in string['vertices']:
				VerticesIncomeZone.objects.create(xCoord = i['x'], yCoord = i['y'], \
				 IncomeZone_id=zoneId)
		#добавить зону исключения
		if string['method'] == 'addexclude':
			zone = ExcludeZone.objects.create(LoadLandscape_id=landscape_id)
			zoneId = zone.id
			for i in string['vertices']:
				VerticesExcludeZone.objects.create(xCoord=i['x'], yCoord=i['y'], \
					ExcludeZone_id=zoneId)
			args['ezones'] = ExcludeZone.objects.filter(LoadLandscape_id=landscape_id)
			return render(request, 'excludezonetable.html', args)
		#удалить зону входа
		if string['method'] == 'delete':
			zoneid = string['zoneid']
			IncomeZone.objects.filter(id=zoneid).delete()
		#удалить зону исключения
		if string['method'] == 'delete_exclude':
			zoneid = string['zoneid']
			ExcludeZone.objects.filter(id=zoneid).delete()
			args['ezones'] = ExcludeZone.objects.filter(LoadLandscape_id=landscape_id)
			return render(request, 'excludezonetable.html', args)
		#привязать зону входа
		if string['method'] == 'link':
			zoneid = string['zoneid']
			if string['type'] == 'building':
				bid = string['id']
				b = Building.objects.get(id=bid)
				zmin = b.minz
				zmax = b.maxz
				# устанавливаем z для зоны по привязанномуэлементу
				VerticesIncomeZone.objects.filter(IncomeZone_id=zoneid).update(zmin=zmin, \
				 zmax=zmax)
				# удаляем ранние привязки
				delZones(zoneid, 'income')
				# сцепляем зону с объектом
				BuildingIncomeZone.objects.create(Building_id=bid, IncomeZone_id=zoneid)
			elif string['type'] == 'floor':
				fid = string['id']
				f = Floor.objects.get(id=fid)
				zmin = f.minz
				zmax = f.maxz
				# устанавливаем z для зоны по привязанномуэлементу
				VerticesIncomeZone.objects.filter(IncomeZone_id=zoneid).update(zmin=zmin, \
					zmax=zmax)
				# удаляем ранние привязки
				delZones(zoneid, 'income')
				# сцепляем зону с объектом
				FloorIncomeZone.objects.create(Floor_id=fid, IncomeZone_id=zoneid)
			elif string['type'] == 'kabinet':
				kid = string['id']
				k = Kabinet_n_Outer.objects.get(id=kid)
				zmin = k.minz
				zmax = k.maxz
				# устанавливаем z для зоны по привязанномуэлементу
				VerticesIncomeZone.objects.filter(IncomeZone_id=zoneid).update(zmin=zmin, \
				 zmax=zmax)
				# удаляем ранние привязки
				delZones(zoneid, 'income')
				# сцепляем зону с объектом
				KabinetIncomeZone.objects.create(Kabinet_id=kid, IncomeZone_id=zoneid)
		# привязать зону исключения
		if string['method'] == 'link_exclude':
			zoneid = string['zoneid']
			if string['type'] == 'building':
				bid = string['id']
				b = Building.objects.get(id=bid)
				zmin = b.minz
				zmax = b.maxz
				# устанавливаем z для зоны по привязанномуэлементу
				VerticesExcludeZone.objects.filter(ExcludeZone_id=zoneid).update(zmin=zmin, \
				 zmax=zmax)
				# удаляем ранние привязки
				delZones(zoneid, 'exclude')
				# сцепляем зону с объектом
				BuildingExcludeZone.objects.create(Building_id=bid, ExcludeZone_id=zoneid)
			elif string['type'] == 'floor':
				fid = string['id']
				f = Floor.objects.get(id=fid)
				zmin = f.minz
				zmax = f.maxz
				# устанавливаем z для зоны по привязанномуэлементу
				VerticesExcludeZone.objects.filter(ExcludeZone_id=zoneid).update(zmin=zmin, \
					zmax=zmax)
				# удаляем ранние привязки
				delZones(zoneid, 'exclude')
				# сцепляем зону с объектом
				FloorExcludeZone.objects.create(Floor_id=fid, ExcludeZone_id=zoneid)
			elif string['type'] == 'kabinet':
				kid = string['id']
				k = Kabinet_n_Outer.objects.get(id=kid)
				zmin = k.minz
				zmax = k.maxz
				# устанавливаем z для зоны по привязанномуэлементу
				VerticesExcludeZone.objects.filter(ExcludeZone_id=zoneid).update(zmin=zmin, \
				 zmax=zmax)
				# удаляем ранние привязки
				delZones(zoneid, 'exclude')
				# сцепляем зону с объектом
				KabinetExcludeZone.objects.create(Kabinet_id=kid, ExcludeZone_id=zoneid)
			args['ezones'] = ExcludeZone.objects.filter(LoadLandscape_id=landscape_id)
			return render(request, 'excludezonetable.html', args)
		# отцепить incomezone
		if string['method'] == 'unlink':
			zoneid = string['zoneid']
			delZones(zoneid, 'income')
		# отцепить excludezone
		if string['method'] == 'unlink_exclude':
			zoneid = string['zoneid']
			delZones(zoneid, 'exclude')
			args['ezones'] = ExcludeZone.objects.filter(LoadLandscape_id=landscape_id)
			return render(request, 'excludezonetable.html', args)
		# сохраняем максимальные или минимальные значения высоты зоны incomezone
		if string['method'] == 'savemin':
			zoneid = string['zoneid']
			value = string['value']
			VerticesIncomeZone.objects.filter(IncomeZone_id=zoneid).update(zmin=value)
		if string['method'] == 'savemax':
			zoneid = string['zoneid']
			value = string['value']
			VerticesIncomeZone.objects.filter(IncomeZone_id=zoneid).update(zmax=value)
		# сохраняем максимальные или минимальные значения высоты зоны excludezone
		if string['method'] == 'savemin_exclude':
			zoneid = string['zoneid']
			value = string['value']
			VerticesExcludeZone.objects.filter(ExcludeZone_id=zoneid).update(zmin=value)
			args['ezones'] = ExcludeZone.objects.filter(LoadLandscape_id=landscape_id)
			return render(request, 'excludezonetable.html', args)
		if string['method'] == 'savemax_exclude':
			zoneid = string['zoneid']
			value = string['value']
			VerticesExcludeZone.objects.filter(ExcludeZone_id=zoneid).update(zmax=value)
			args['ezones'] = ExcludeZone.objects.filter(LoadLandscape_id=landscape_id)
			return render(request, 'excludezonetable.html', args)
		# возвращаем зоны, привязанные к объекту, чтобы их окрасить в таблице incomezone
		if string['method'] == 'colored':
			dae_name = string['dae_name']
			if string['type'] == 'building':
				b = Building.objects.get(LoadLandscape_id=landscape_id, dae_BuildingName=dae_name)
				args['colored'] = BuildingIncomeZone.objects.filter(Building_id=b.id)
			elif string['type'] == 'floor':
				f = Floor.objects.get(LoadLandscape_id=landscape_id, dae_FloorName=dae_name)
				args['colored'] = FloorIncomeZone.objects.filter(Floor_id=f.id)
			elif string['type'] == 'kabinet':
				k = Kabinet_n_Outer.objects.get(LoadLandscape_id=landscape_id, \
				 dae_Kabinet_n_OuterName=dae_name)
				args['colored'] = KabinetIncomeZone.objects.filter(Kabinet_id=k.id)
		# возвращаем зоны, привязанные к объекту, чтобы их окрасить в таблице excludezone
		if string['method'] == 'colored_exclude':
			dae_name = string['dae_name']
			if string['type'] == 'building':
				b = Building.objects.get(LoadLandscape_id=landscape_id, dae_BuildingName=dae_name)
				args['colored'] = BuildingExcludeZone.objects.filter(Building_id=b.id)
			elif string['type'] == 'floor':
				f = Floor.objects.get(LoadLandscape_id=landscape_id, dae_FloorName=dae_name)
				args['colored'] = FloorExcludeZone.objects.filter(Floor_id=f.id)
			elif string['type'] == 'kabinet':
				k = Kabinet_n_Outer.objects.get(LoadLandscape_id=landscape_id, \
				 dae_Kabinet_n_OuterName=dae_name)
				args['colored'] = KabinetExcludeZone.objects.filter(Kabinet_id=k.id)
			args['ezones'] = ExcludeZone.objects.filter(LoadLandscape_id=landscape_id)
			return render(request, 'excludezonetable.html', args)
		# показываем запрашиваемую зону incomezone
		if string['method'] == 'show':
			obj = {}
			obj['izone']  = []
			zoneid = string['zoneid']
			vertices = VerticesIncomeZone.objects.filter(IncomeZone_id=zoneid)
			vToSend = []
			for v in vertices:
				vToSend.append({'x': v.xCoord, 'y': v.yCoord, 'zmin': v.zmin, 'zmax': v.zmax})
			obj['izone'].append({'id': zoneid, 'vertices': vToSend, \
				'faces': getFacesFromVert(vToSend)})
			return JsonResponse(obj)
		# показываем запрашиваемую зону excludezone
		if string['method'] == 'show_exclude':
			obj = {}
			obj['ezone']  = []
			zoneid = string['zoneid']
			vertices = VerticesExcludeZone.objects.filter(ExcludeZone_id=zoneid)
			vToSend = []
			for v in vertices:
				vToSend.append({'x': v.xCoord, 'y': v.yCoord, 'zmin': v.zmin, 'zmax': v.zmax})
			obj['ezone'].append({'id': zoneid, 'vertices': vToSend, \
				'faces': getFacesFromVert(vToSend)})
			return JsonResponse(obj)
		# формируем словарь с вершинами объекта
		if string['method'] == 'objvertices':
			obj = {}
			dae_name = string['dae_name']
			obj['vertices'] = []
			if string['type'] == 'building':
				obj['type'] = 'building'
				b = Building.objects.get(LoadLandscape_id=landscape_id, dae_BuildingName=dae_name)
				obj['minz'] = b.minz
				obj['maxz'] = b.maxz
				verticesbuilding = VerticesBuilding.objects.filter(Building_id=b.id)
				for v in verticesbuilding:
					obj['vertices'].append([v.x, v.y])
				# ищем зоны входа для building
				zones = BuildingIncomeZone.objects.filter(Building_id=b.id)
				obj['izone'] = []
				for z in zones:
					zoneid = z.IncomeZone_id
					# вершины
					vertices = VerticesIncomeZone.objects.filter(IncomeZone_id=zoneid)
					vToSend = []
					for v in vertices:
						vToSend.append({'x': v.xCoord, 'y': v.yCoord, 'zmin': v.zmin, 'zmax': v.zmax})
					obj['izone'].append({'id': z.IncomeZone_id, 'vertices': vToSend, \
					 'faces': getFacesFromVert(vToSend)})
				# ищем зоны исключения для building
				zones = BuildingExcludeZone.objects.filter(Building_id=b.id)
				obj['ezone'] = []
				for z in zones:
					zoneid = z.ExcludeZone_id
					# вершины
					vertices = VerticesExcludeZone.objects.filter(ExcludeZone_id=zoneid)
					vToSend = []
					for v in vertices:
						vToSend.append({'x': v.xCoord, 'y': v.yCoord, 'zmin': v.zmin, 'zmax': v.zmax})
					obj['ezone'].append({'id': z.ExcludeZone_id, 'vertices': vToSend, \
					 'faces': getFacesFromVert(vToSend)})
			elif string['type'] == 'floor':
				obj['type'] = 'floor'
				f = Floor.objects.get(LoadLandscape_id=landscape_id, dae_FloorName=dae_name)
				obj['minz'] = f.minz
				obj['maxz'] = f.maxz
				verticesfloor = VerticesFloor.objects.filter(Floor_id=f.id)
				for v in verticesfloor:
					obj['vertices'].append([v.x, v.y])
				# ищем зоны входа для floor
				zones = FloorIncomeZone.objects.filter(Floor_id=f.id)
				obj['izone'] = []
				for z in zones:
					zoneid = z.IncomeZone_id
					# вершины
					vertices = VerticesIncomeZone.objects.filter(IncomeZone_id=zoneid)
					vToSend = []
					for v in vertices:
						vToSend.append({'x': v.xCoord, 'y': v.yCoord, 'zmin': v.zmin, 'zmax': v.zmax})
					obj['izone'].append({'id': z.IncomeZone_id, 'vertices': vToSend, \
						'faces': getFacesFromVert(vToSend)})
				# ищем зоны исключения для floor
				zones = FloorExcludeZone.objects.filter(Floor_id=f.id)
				obj['ezone'] = []
				for z in zones:
					zoneid = z.ExcludeZone_id
					# вершины
					vertices = VerticesExcludeZone.objects.filter(ExcludeZone_id=zoneid)
					vToSend = []
					for v in vertices:
						vToSend.append({'x': v.xCoord, 'y': v.yCoord, 'zmin': v.zmin, 'zmax': v.zmax})
					obj['ezone'].append({'id': z.ExcludeZone_id, 'vertices': vToSend, \
						'faces': getFacesFromVert(vToSend)})
			elif string['type'] == 'kabinet':
				obj['type'] = 'kabinet'
				k = Kabinet_n_Outer.objects.get(LoadLandscape_id=landscape_id, \
				 dae_Kabinet_n_OuterName=dae_name)
				obj['minz'] = k.minz
				obj['maxz'] = k.maxz
				verticeskabinet = VerticesKabinet_n_Outer.objects.filter(Kabinet_n_Outer_id=k.id)
				for v in verticeskabinet:
					obj['vertices'].append([v.x, v.y])
				# ищем зоны входа для kabinet
				zones = KabinetIncomeZone.objects.filter(Kabinet_id=k.id)
				obj['izone'] = []
				for z in zones:
					zoneid = z.IncomeZone_id
					# вершины
					vertices = VerticesIncomeZone.objects.filter(IncomeZone_id=zoneid)
					vToSend = []
					for v in vertices:
						vToSend.append({'x': v.xCoord, 'y': v.yCoord, 'zmin': v.zmin, 'zmax': v.zmax})
					obj['izone'].append({'id': z.IncomeZone_id, 'vertices': vToSend, \
						'faces': getFacesFromVert(vToSend)})
				# ищем зоны исключения для kabinet
				zones = KabinetExcludeZone.objects.filter(Kabinet_id=k.id)
				obj['ezone'] = []
				for z in zones:
					zoneid = z.ExcludeZone_id
					# вершины
					vertices = VerticesExcludeZone.objects.filter(ExcludeZone_id=zoneid)
					vToSend = []
					for v in vertices:
						vToSend.append({'x': v.xCoord, 'y': v.yCoord, 'zmin': v.zmin, 'zmax': v.zmax})
					obj['ezone'].append({'id': z.ExcludeZone_id, 'vertices': vToSend, \
						'faces': getFacesFromVert(vToSend)})
			return JsonResponse(obj)
		args['zones'] = IncomeZone.objects.filter(LoadLandscape_id=landscape_id)
		return render(request, 'incomezonetable.html', args)
	return render(request, 'incomezonedefine.html', args)

#поверхности
def getFacesFromVert(arr):
	face = []
	for i in range(0, len(arr), 1):
		if i == 0:
			a = 0
			b = i+1
			c = i+2
			face.append({'a': a, 'b': b, 'c': c})
		elif i < len(arr):
			a = 0
			b = i-1
			c = i
			face.append({'a': a, 'b': b, 'c': c})
	return face		
# сортировка вершин	
def sortVert(arr):
	if len(arr) > 0:
		pp = arr
		cent  = (sum([p[0] for p in pp])/len(pp), sum([p[1] for p in pp])/len(pp))
		pp.sort(key=lambda p: math.atan2(p[1]-cent[1], p[0]-cent[0]))
		return pp
	else:
		return False
# функция удаления зон
def delZones(zoneid, text):
	if text == 'income':
		BuildingIncomeZone.objects.filter(IncomeZone_id=zoneid).delete()
		FloorIncomeZone.objects.filter(IncomeZone_id=zoneid).delete()
		KabinetIncomeZone.objects.filter(IncomeZone_id=zoneid).delete()
	elif text == 'exclude':
		BuildingExcludeZone.objects.filter(ExcludeZone_id=zoneid).delete()
		FloorExcludeZone.objects.filter(ExcludeZone_id=zoneid).delete()
		KabinetExcludeZone.objects.filter(ExcludeZone_id=zoneid).delete()