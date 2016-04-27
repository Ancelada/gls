#!/usr/bin/python
# -*- coding: utf8 -*-
from django.template.loader import render_to_string
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
	url = 'http://192.168.1.111:8000'
	data = json({"SESSION":{"ID":0,"Name":"КБНТ","Password":"1234","ID_layer":3,"Inuse":1},"LAYER":{"ID":3,"Name":"Подложка КБНТ","Latitude_1":0,"Longitude_1":0,"Height_1":0,"X_1":0,"Y_1":0,"Z_1":0,"Latitude_2":0,"Longitude_2":0,"Height_2":0,"X_2":149.9980484375,"Y_2":0,"Z_2":149.9980484375,"ScaleX":0,"ScaleY":0},"Plans":[{"ID":13,"Name":"building_001","Description":"","X":70.74239957130649,"Y":0.010000229813150255,"Z":71.06670148823082,"Sizex":48.16391453965018,"Sizey":9.184015239940116,"Sizez":29.859846559427446,"AngleRotateX":0,"AngleRotateY":0,"AngleRotateZ":0,"ObjType":2},{"ID":15,"Name":"floor_003","Description":"","X":70.74239957130649,"Y":5.999999999999999,"Z":71.06210742988696,"Sizex":48.16391453965018,"Sizey":3.194015469753267,"Sizez":29.850658442739736,"AngleRotateX":0,"AngleRotateY":0,"AngleRotateZ":0,"ObjType":3},{"ID":17,"Name":"kabinet_001","Description":"","X":72.9144675778225,"Y":6.110000133514401,"Z":79.98160425567863,"Sizex":18.110019216313958,"Sizey":3.0700001716613823,"Sizez":11.89002005767351,"AngleRotateX":0,"AngleRotateY":0,"AngleRotateZ":0,"ObjType":4},{"ID":23,"Name":"kabinet_002","Description":"","X":72.51891588192211,"Y":5.999999999999999,"Z":69.24602592323852,"Sizex":44.37210082571874,"Sizey":3.1328890260732303,"Sizez":10.169453317166443,"AngleRotateX":0,"AngleRotateY":0,"AngleRotateZ":0,"ObjType":4},{"ID":27,"Name":"kabinet_003","Description":"","X":92.20149188194193,"Y":5.999999999999999,"Z":60.668667064128414,"Sizex":5.245729918379311,"Sizey":3.1077058552103063,"Sizez":7.649775110288083,"AngleRotateX":0,"AngleRotateY":0,"AngleRotateZ":0,"ObjType":4},{"ID":31,"Name":"kabinet_004","Description":"","X":86.59412272392112,"Y":6,"Z":61.93489222452154,"Sizex":5.955031855410439,"Sizey":3.101723422519566,"Sizez":10.203969839997669,"AngleRotateX":0,"AngleRotateY":0,"AngleRotateZ":0,"ObjType":4},{"ID":35,"Name":"kabinet_005","Description":"","X":80.91715632722644,"Y":6,"Z":61.94667494352351,"Sizex":5.2688153892362095,"Sizey":3.124796228881836,"Sizez":10.262474647165433,"AngleRotateX":0,"AngleRotateY":0,"AngleRotateZ":0,"ObjType":4},{"ID":39,"Name":"kabinet_006","Description":"","X":75.2422464226176,"Y":6,"Z":61.933724485977294,"Sizex":5.98672110782509,"Sizey":3.0478870478096596,"Sizez":10.19438963302148,"AngleRotateX":0,"AngleRotateY":0,"AngleRotateZ":0,"ObjType":4},{"ID":43,"Name":"kabinet_007","Description":"","X":69.54112600361192,"Y":6,"Z":64.89486433185898,"Sizex":5.37559170725271,"Sizey":3.0555796743794676,"Sizez":4.24365943164765,"AngleRotateX":0,"AngleRotateY":0,"AngleRotateZ":0,"ObjType":4},{"ID":47,"Name":"kabinet_008","Description":"","X":63.89833357800467,"Y":6,"Z":64.93468673978906,"Sizex":5.854764554511924,"Sizey":3.106966228881836,"Sizez":4.243269402000003,"AngleRotateX":0,"AngleRotateY":0,"AngleRotateZ":0,"ObjType":4},{"ID":53,"Name":"kabinet_009","Description":"","X":63.82241659334213,"Y":6,"Z":61.88359489494879,"Sizex":16.82601360632721,"Sizey":3.1632532288818407,"Sizez":10.163494913982063,"AngleRotateX":0,"AngleRotateY":0,"AngleRotateZ":0,"ObjType":4},{"ID":57,"Name":"kabinet_010","Description":"","X":58.10941105118468,"Y":6,"Z":70.66129678158688,"Sizex":6.354355620040479,"Sizey":3.120327359353304,"Sizez":2.645706873687189,"AngleRotateX":0,"AngleRotateY":0,"AngleRotateZ":0,"ObjType":4},{"ID":61,"Name":"kabinet_011","Description":"","X":62.99635928626192,"Y":6,"Z":70.67996136315274,"Sizex":3.3581496804027395,"Sizey":3.1183888583329917,"Sizez":2.6052768063805445,"AngleRotateX":0,"AngleRotateY":0,"AngleRotateZ":0,"ObjType":4},{"ID":65,"Name":"kabinet_012","Description":"","X":65.90757486428046,"Y":6,"Z":70.71524319026662,"Sizex":2.420035511649999,"Sizey":3.134411111505031,"Sizez":2.5617481023136293,"AngleRotateX":0,"AngleRotateY":0,"AngleRotateZ":0,"ObjType":4},{"ID":69,"Name":"kabinet_013","Description":"","X":67.91184279369476,"Y":6,"Z":70.69608339195581,"Sizex":1.5192016254815712,"Sizey":3.134412042652368,"Sizez":2.556848388325676,"AngleRotateX":0,"AngleRotateY":0,"AngleRotateZ":0,"ObjType":4},{"ID":73,"Name":"kabinet_014","Description":"","X":72.522261766453,"Y":6,"Z":70.69830815305204,"Sizex":7.66586612104345,"Sizey":3.1344122288818355,"Sizez":2.568787540280354,"AngleRotateX":0,"AngleRotateY":0,"AngleRotateZ":0,"ObjType":4},{"ID":77,"Name":"kabinet_015","Description":"","X":77.27579110758651,"Y":6,"Z":70.68853121335937,"Sizex":1.7775514045543162,"Sizey":3.1344122288818355,"Sizez":2.5178912158343536,"AngleRotateX":0,"AngleRotateY":0,"AngleRotateZ":0,"ObjType":4},{"ID":81,"Name":"kabinet_017","Description":"","X":85.07017858027069,"Y":6,"Z":70.6938714410664,"Sizex":4.392652956118781,"Sizey":3.0863442288818366,"Sizez":2.5022070379999946,"AngleRotateX":0,"AngleRotateY":0,"AngleRotateZ":0,"ObjType":4},{"ID":85,"Name":"kabinet_016","Description":"","X":80.54440633326456,"Y":6.000004768371582,"Z":70.69388565443359,"Sizex":4.67923375427435,"Sizey":1.7763568394002505e-15,"Sizez":2.467183329000008,"AngleRotateX":0,"AngleRotateY":0,"AngleRotateZ":0,"ObjType":4},{"ID":87,"Name":"kabinet","Description":"","X":48.477298887531916,"Y":6,"Z":71.37049910402754,"Sizex":3.633713172101018,"Sizey":3.194015469753266,"Sizez":5.806939889274574,"AngleRotateX":0,"AngleRotateY":0,"AngleRotateZ":0,"ObjType":4},{"ID":91,"Name":"floor_002","Description":"","X":70.74233704784241,"Y":2.980000734329195,"Z":71.06722375805089,"Sizex":48.02156091300267,"Sizey":3.089999318122917,"Sizez":29.858802019787312,"AngleRotateX":0,"AngleRotateY":0,"AngleRotateZ":0,"ObjType":3},{"ID":95,"Name":"kabinet_000","Description":"","X":114.73401555923473,"Y":2.980000734329223,"Z":62.10613902624419,"Sizex":44.21847833673684,"Sizey":3.0100003944189617,"Sizez":14.101679868993607,"AngleRotateX":0,"AngleRotateY":-3.1415925561171143,"AngleRotateZ":0,"ObjType":4},{"ID":99,"Name":"floor_001","Description":"","X":70.74233717880966,"Y":0.010000229813150255,"Z":71.06722375805089,"Sizex":48.021560651068164,"Sizey":3.0100002298131887,"Sizez":29.858802019787312,"AngleRotateX":0,"AngleRotateY":0,"AngleRotateZ":0,"ObjType":3}],"PLANS_TREE":[{"ID":13,"IDParent":-1},{"ID":15,"IDParent":13},{"ID":17,"IDParent":15},{"ID":23,"IDParent":15},{"ID":27,"IDParent":15},{"ID":31,"IDParent":15},{"ID":35,"IDParent":15},{"ID":39,"IDParent":15},{"ID":43,"IDParent":15},{"ID":47,"IDParent":15},{"ID":53,"IDParent":15},{"ID":57,"IDParent":15},{"ID":61,"IDParent":15},{"ID":65,"IDParent":15},{"ID":69,"IDParent":15},{"ID":73,"IDParent":15},{"ID":77,"IDParent":15},{"ID":81,"IDParent":15},{"ID":85,"IDParent":15},{"ID":87,"IDParent":15},{"ID":91,"IDParent":13},{"ID":95,"IDParent":91},{"ID":99,"IDParent":13}]})
	headers = {'content-type:': 'application/json', 'charset': 'utf-8'}
	r = requests.post(url, data=data, headers=headers)
	json_data = json(r.text)
	return HttpResponse(json_data)

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

# фунцкия проверки правильности заолнения словаря userzones
def getuzones(request, parameters=''):
	landscape_id = parameters
	for i in static:
		if i['landscape_id'] == parameters:
			return HttpResponse(i['userzones'])

def filluzones(user_id, landscape_id):
	uzones = UserZone.objects.all()
	vuzones = VerticesUserZone.objects.all()
	izuzones = IncomeZoneUserZone.objects.all()
	ezuzones = ExcludeZoneUserZone.objects.all()
	vizones = VerticesIncomeZone.objects.all()
	vezones = VerticesExcludeZone.objects.all()
	arr = []
	no = 0
	for uzone in uzones:
		if uzone.LoadLandscape_id==landscape_id and uzone.User_id==user_id:
			arr.append({'id': uzone.id, 'vertices': [], 'minz': 0, 'maxz': 0, \
			 'IncomeZones': [], 'ExcludeZones': []})
			# maxz minz
			for vuzone in vuzones:
				if vuzone.UserZone_id == uzone.id:
					minz = vuzone.zmin
					maxz = vuzone.zmax
					arr[no]['minz'] = minz
					arr[no]['maxz'] = maxz
					break
			# наполняем uzone вершинами
			for vuzone in vuzones:
				if vuzone.UserZone_id == arr[no]['id']:
					arr[no]['vertices'].append([float(vuzone.xCoord), float(vuzone.yCoord)])
					#сортировка вершин
					a = sortVert(arr[no]['vertices'])
					arr[no]['vertices'] = a
			# наполняем IncomeZones
			izno = 0
			for izuz in izuzones:
				if izuz.UserZone_id == uzone.id:
					arr[no]['IncomeZones'].append({'id': izuz.IncomeZone_id, 'vertices': [], \
					 'minz': 0, 'maxz': 0})
					# наполняем vertices incomezone
					for v in vizones:
						if v.IncomeZone_id == izuz.IncomeZone_id:
							arr[no]['IncomeZones'][izno]['vertices'].append([float(v.xCoord), float(v.yCoord)])
							minz = v.zmin
							maxz = v.zmax
					a = sortVert(arr[no]['IncomeZones'][izno]['vertices'])
					arr[no]['IncomeZones'][izno]['vertices'] = a
					# minz maxz
					arr[no]['IncomeZones'][izno]['minz'] = minz
					arr[no]['IncomeZones'][izno]['maxz'] = maxz
					izno += 1
			ezno = 0
			# наполняем ExcludeZones
			for ezuz in ezuzones:
				if ezuz.UserZone_id == uzone.id:
					arr[no]['ExcludeZones'].append({'id': ezuz.ExcludeZone_id, 'vertices': [], \
						'minz': 0, 'maxz': 0})
					# наполняем vertices excludezone
					for v in vezones:
						if v.ExcludeZone_id == ezuz.ExcludeZone_id:
							arr[no]['ExcludeZones'][ezno]['vertices'].append([float(v.xCoord), float(v.yCoord)])
							minz = v.zmin
							maxz = v.zmax
					a = sortVert(arr[no]['ExcludeZones'][ezno]['vertices'])
					arr[no]['ExcludeZones'][ezno]['vertices'] = a
					# minz maxz
					arr[no]['ExcludeZones'][ezno]['minz'] = minz
					arr[no]['ExcludeZones'][ezno]['maxz'] = maxz
					ezno += 1
			no += 1
	return arr

# наполняем статику
def fillStatic():
	landscape = LoadLandscape.objects.all()
	users = User.objects.all()
	for l in landscape:
		static.append({'landscape_id': l.landscape_id, 'buildings': [], 'userzones': []})
		for i in static:
			if i['landscape_id'] == l.landscape_id:
				#прежде чем заполнить статику, заполняем зоны пользователя на каждой сцене
				#filluserzones at each landscape
				uzno = 0
				for u in users:
					i['userzones'].append({'user_id': u.id, 'uzones': []})
					#наполняем uzones
					i['userzones'][uzno]['uzones'] = filluzones(u.id, l.landscape_id)
					uzno+=1
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

def getuniquevalues2(request, parameters=''):
	for i in unique:
		if i['tag_id'] == parameters:
			return HttpResponse(i['userzone'])
	return HttpResponse('something is wrong')

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

#отправка сообщения unique удалить или добавить метку
def updateUnique(unique, msgtype):
	for i in active_users:
		try:
			if msgtype == 'delete':
				service_queue('update_unique', \
				 json({'user': i['id'],'data': {'tag': unique, 'type': 'delete'}}))
			elif msgtype == 'add':
				rendered = render_to_string('addlineuniquetodynamic.html', {'tag_id': unique['tag_id']})
				service_queue('update_unique', json({'user': i['id'], \
				 'data': {'tag': unique, 'type': 'add', \
					'rendered': rendered}}))
		except:
			pass



#плавная unique корректировка
def correctF():
	for i in unique:
		if 'cron' in i and i['cron'] > 20:
			updateUnique(i, 'delete')
			try:
				t = Tag.objects.get(TagId=i['tag_id'])
				TurnOnOffTag(OnOff=0, OnOffTime=datetime.datetime.now(), Tag_id=t.TagId, \
				 LoadLandscape_id=i['zone_id']).save()
				unique.remove(i)
			except:
				unique.remove(i)
			break
	for i in unique:
		if 'cron' in i:
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
		arr = []
		for j in unique:
			if 'vertices' in i:
				if inObject(i, j['x'], j['y'], j['z']):
					arr.append(j)
		try:
			service_queue('coords_server_lock', json({'user': i['id'],'data': arr}))
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
				# ищем подходящие зоны пользователя
				findMatchingUserZone(i, i['zone_id'])

#ищем подходящую userzone
def findMatchingUserZone(obj, landscape_id):
	x = obj['x']
	y = obj['y']
	z = obj['z']
	# добавляем словарь userzone к объекту
	if not 'userzone' in obj:
		obj['userzone'] = []
		# к словарю добавляем всех пользователей
		for uzone in static[0]['userzones']:
			obj['userzone'].append({'user_id': uzone['user_id'], 'noUserZoneLocation': {'cron': 0}, \
				 'candidate': [], 'UserZoneLocation': {'type': 'outofzone', 'id': 0}})
	# если отсутствует candidate
	# включаем хронометраж
	objno = 0
	for user in obj['userzone']:
		if not 'candidate' in user or len(user['candidate']) == 0:
			if not 'noUserZoneLocation' in user:
				user['noUserZoneLocation'] = {'cron': 0}
			else:
				user['noUserZoneLocation']['cron'] += 1
			# проверка достигнуто ли noUserZoneLocation cron значения 10
			# если достигнуло , то UserZoneLocation очищаем
			if user['noUserZoneLocation']['cron'] == 10:
				if user['UserZoneLocation']['type'] == 'inuzone':
					user['UserZoneLocation'] = {'type': 'outofzone', 'id': 0}
					# записываем в БД выход из зон TagNoUzone
					try:
						TagNoUzone.objects.create(User_id=user['user_id'], Tag_id=obj['tag_id'], \
							 WriteTime=datetime.datetime.now(), LoadLandscape_id=obj['zone_id'])
					except:
						pass
			elif user['noUserZoneLocation']['cron'] == 100:
				user['noUserZoneLocation']['cron'] = 0
		elif len(user['candidate']) > 0 and 'candidate' in user:
			user['noUserZoneLocation']['cron'] = 0
		if 'candidate' in user:
			#удаляем просроченные candidate
			deleteFromListByKeyValueUpper(20, 'cron', user['candidate'])
			# увеличиваем cron
			for i in user['candidate']:
				i['cron'] += 1
			#проверка есть ли candidate incomezone в списке incomezone если cron == 7,
			# и matchCount > 4
			for i in user['candidate']:
				if i['cron'] == 7 and i['matchCount'] > 4:
					for caniz in i['IncomeZones']:
						candidateincomezone = caniz['id']
						for objiz in obj['IncomeZones']:
							if objiz['id'] == candidateincomezone:
								if 'UserZoneLocation' in user:
									if user['UserZoneLocation']['id'] != i['id']:
										user['UserZoneLocation']['id'] = i['id']
										user['UserZoneLocation']['type'] = 'inuzone'
										# записываем в БД TagUzoneUserOrder событие
										try:
											TagUzoneUserOrder.objects.create(Tag_id=obj['tag_id'], \
												User_id=user['user_id'], \
												 UserZone_id=user['UserZoneLocation']['id'], \
												 WriteTime=datetime.datetime.now())
										except:
											pass
										#очищаем Candidate и IncomeZones
										del user['candidate'][:]
								else:
									user['UserZoneLocation'] = {'id': i['id'], 'type': 'inuzone'}
									#очищаем Candidate и IncomeZones
									del user['candidate'][:]
				#проверка если candidate incomezone отсутствует в incomezone cron == 20, 
				# matchCount > 15
				elif i['cron'] == 20 and i['matchCount']>15:
					if 'UserZoneLocation' in user:
						if user['UserZoneLocation']['id'] != i['id']:
							user['UserZoneLocation']['id'] = i['id']
							user['UserZoneLocation']['type'] = 'inuzone'
							# записываем в БД TagUzoneUserOrder событие
							try:
								TagUzoneUserOrder.objects.create(Tag_id=obj['tag_id'], \
									User_id=user['user_id'], \
									 UserZone_id=user['UserZoneLocation']['id'], \
									 WriteTime=datetime.datetime.now())
							except:
								pass
							#очищаем Candidate и IncomeZones
							del user['candidate'][:]
					else:
						user['UserZoneLocation'] = {'id': i['id'], 'type': 'inuzone'}
						#очищаем Candidate и IncomeZones
						del user['candidate'][:]
		# добавить userzones в candidate
		user_id = user['user_id']
		for s in static:
			for uz in s['userzones']:
				if uz['user_id'] == user_id:
					inuz = 0
					for userzone in uz['uzones']:
						# проверка попадания точки в userzone
						if not(inExcludeZone(userzone, x, y, z)) and inObject(userzone, x, y, z):
							inuz = 1
						# проверить есть ли userzone в candidate
						if inuz:
							if 'candidate' in user:
								doubled = 0
								for c in user['candidate']:
									if c['id'] == userzone['id']:
										doubled = 1
									# увеличиваем matchCount
									c['matchCount'] += 1
								if not doubled:
									user['candidate'].append({'id': userzone['id'], \
										 'cron': 0, 'matchCount': 0, 'IncomeZones': \
										  userzone['IncomeZones']})
							break
		objno += 1
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
									# записываем в отчеты БД TagKabinetOrder
									try:
										TagKabinetOrder.objects.create(Tag_id=obj['tag_id'], \
											 Kabinet_n_Outer_id=obj['location']['id'], \
											  WriteTime=datetime.datetime.now())
									except:
										pass
									#очищаем Candidate и IncomeZones
									del obj['candidate'][:]
									del obj['IncomeZones'][:]
							else:
								obj['location'] = {'id': i['id'], 'type': 'kabinet'
								}
								# записываем в отчеты БД TagKabinetOrder 
								try:
									TagKabinetOrder.objects.create(Tag_id=obj['tag_id'], \
										 Kabinet_n_Outer_id=obj['location']['id'], \
										  WriteTime=datetime.datetime.now())
								except:
									pass
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
						# записываем в отчеты БД TagKabinetOrder
						try:
							TagKabinetOrder.objects.create(Tag_id=obj['tag_id'], \
								 Kabinet_n_Outer_id=obj['location']['id'], \
								  WriteTime=datetime.datetime.now())
						except:
							pass
						#очищаем Candidate и IncomeZones
						del obj['candidate'][:]
						del obj['IncomeZones'][:]
				else:
					obj['location'] = {'id': i['id'], 'type': 'kabinet'}
					# записываем в отчеты БД TagKabinetOrder
					try:
						TagKabinetOrder.objects.create(Tag_id=obj['tag_id'], \
							 Kabinet_n_Outer_id=obj['location']['id'], \
							  WriteTime=datetime.datetime.now())
					except:
						pass
					#очищаем Candidate и IncomeZones
					del obj['candidate'][:]
					del obj['IncomeZones'][:]
	x = obj['x']
	y = obj['y']
	z = obj['z']
	for s in static:
		if s['landscape_id'] == landscape_id:
			inBld = 0
			for building in s['buildings']:
				#проверка попадание в здание
				#если нет candidates
				if not(inExcludeZone(building, x, y, z)) and inObject(building, x, y,z ):
					inBld = 1
				if 'notInBuild' in obj:
					# фиксируем выход из здания
					# 5 секунд, если есть попадание в incomezone building 4 раза
					if obj['notInBuild']['cron'] == 5 and obj['notInBuild']['match'] > 4:
						buildingincomezone = building['IncomeZones']
						for iz in obj['IncomeZones']:
							for biz in buildingincomezone:
								if iz['id'] == biz['id']:
									if 'location' in obj:
										if obj['location']['type'] != 'street':
											obj['location'] = {'type': 'street', 'id': 0}
											# записываем событие в БД TagOutOfBuilding
											try:
												TagOutOfBuilding.objects.create(Tag_id=obj['tag_id'], \
													WriteTime=datetime.datetime.now(), \
													 LoadLandscape_id=obj['zone_id'])
											except:
												pass
									else:
										obj['location'] = {'type': 'street', 'id': 0}
										# записываем событие в БД TagOutOfBuilding
										try:
											TagOutOfBuilding.objects.create(Tag_id=obj['tag_id'], \
												WriteTime=datetime.datetime.now(), \
												 LoadLandscape_id=obj['zone_id'])
										except:
											pass
									obj['notInBuild'] = {'cron':0, 'match': 0}
									obj['noLocation'] = {'cron': 0}
					# фиксируем выход из здания
					# 20 секунд, если есть попадание в incomezone building 15 раз
					if obj['notInBuild']['cron'] == 19 and obj['notInBuild']['match'] > 15:
						if 'location' in obj:
							if obj['location']['type'] != 'street':
								obj['location'] = {'type': 'street', 'id': 0}
								# записываем событие в БД TagOutOfBuilding
								try:
									TagOutOfBuilding.objects.create(Tag_id=obj['tag_id'], \
										WriteTime=datetime.datetime.now(), \
										 LoadLandscape_id=obj['zone_id'])
								except:
									pass
						else:
							obj['location'] = {'type': 'street', 'id': 0}
							# записываем событие в БД TagOutOfBuilding
							try:
								TagOutOfBuilding.objects.create(Tag_id=obj['tag_id'], \
									WriteTime=datetime.datetime.now(), \
									 LoadLandscape_id=obj['zone_id'])
							except:
								pass
						obj['notInBuild'] = {'cron': 0, 'match': 0}
						obj['noLocation'] = {'cron': 0}
				# фиксация попадания floor на этаж, если отсутствует kabinet
				for floor in building['floors']:
					#если нет candidates, есть зона входа floor, noLocation.cron = 6
					if (obj['noLocation']['cron'] == 6 and 'candidate' in obj and \
					 len(obj['candidate']) == 0) or (obj['noLocation']['cron'] == 6 and \
					  not 'candidate' in obj):
						floorincomezone = floor['IncomeZones']
						inZone = 0
						for oiz in obj['IncomeZones']:
							for fiz in floorincomezone:
								if oiz['id'] == fiz['id']:
									inZone = 1
						if inZone:
							if not(inExcludeZone(floor, x, y, z)) and inObject(floor, x, y, z):
								if 'location' in obj and obj['location']['id'] != floor['id']:
									obj['location'] = {'id': floor['id'], 'type': 'floor'}
									# записываем событие входа на этаж TagFloorOrder
									try:
										TagFloorOrder.objects.create(Tag_id=obj['tag_id'], \
											 Floor_id=floor['id'], WriteTime=datetime.datetime.now())
									except:
										pass
								elif 'location' not in obj:
									obj['location'] = {'id': floor['id'], 'type': 'floor'}
									# записываем событие входа на этаж TagFloorOrder
									try:
										TagFloorOrder.objects.create(Tag_id=obj['tag_id'], \
											 Floor_id=floor['id'], WriteTime=datetime.datetime.now())
									except:
										pass
								obj['noLocation']['cron'] = 0
					# если нет candidates, нет зоны входа floor, noLocation.cron > 20
					if (obj['noLocation']['cron'] > 20 and 'candidate' in obj and \
					 len(obj['candidate']) == 0) or (obj['noLocation']['cron'] > 20 and \
					  not 'candidate' in obj):
						# проверяем, входит ли вектор во floor
						if inObject(floor, x, y, z):
							# проверяем входит ли в зону исключения
							if not(inExcludeZone(floor, x, y, z)):
								if 'location' in obj:
									if obj['location']['id'] != floor['id']:
										obj['location'] = {'id': floor['id'], 'type': 'floor'}
										# записываем событие входа на этаж TagFloorOrder
										try:
											TagFloorOrder.objects.create(Tag_id=obj['tag_id'], \
												 Floor_id=floor['id'], WriteTime=datetime.datetime.now())
										except:
											pass
								else:
									obj['location'] = {'id': floor['id'], 'type': 'floor'}
									# записываем событие входа на этаж TagFloorOrder
									try:
										TagFloorOrder.objects.create(Tag_id=obj['tag_id'], \
											 Floor_id=floor['id'], WriteTime=datetime.datetime.now())
									except:
										pass
								obj['noLocation']['cron'] = 0
					for kabinet in floor['kabinets']:
						#проверяем, входит ли вектор в kabinet
						if inObject(kabinet, x, y, z):
							# проверяем входит ли в зону исключения
							if not (inExcludeZone(kabinet, x, y, z)):
							 	if not 'candidate' in obj:
							 		obj['candidate'] = []
						 		elif not(dictKeyInArray(kabinet['id'], 'id', obj['candidate'], 0)):
									obj['candidate'].append({'id': kabinet['id'], 'cron': 0, \
										'matchCount': 0, 'IncomeZones': kabinet['IncomeZones']})
								#если есть кандидат, зафиксировать попадание в matchCount
								else:
									updateMatchCount(kabinet['id'], 'id', obj['candidate'])
			# фиксация попаданий в здание
			if inBld == 0:
				if not 'notInBuild' in obj:
					obj['notInBuild'] = {'cron': 0, 'match': 0}
				else:
					obj['notInBuild']['match'] += 1
					obj['notInBuild']['cron'] += 1
			elif inBld == 1:
				if 'notInBuild' in obj:
					obj['notInBuild']['cron'] += 1
			if 'notInBuild' in obj and obj['notInBuild']['cron'] == 20:
				obj['notInBuild']['cron'] = 0
				obj['notInBuild']['match'] = 0
# проверка входит ли вектор в объект, без проверки ExcludeZone
def inObject(obj, x, y, z):
	vertices = obj['vertices']
	vector = [(x, y)]
	minz = obj['minz']
	maxz = obj['maxz']
	match = inPolygon(vertices, vector)
	if (match and inInterval(z, minz, maxz)):
		return True
	else:
		return False

# проверка входит ли объект в зону исключения
def inExcludeZone(obj, x, y, z):
	inZone = 0
	vector = [(x, y)]
	for ez in obj['ExcludeZones']:
		vertices = ez['vertices']
		minz = ez['minz']
		maxz = ez['maxz']
		match = inPolygon(vertices, vector)
		if (match and inInterval(z, minz, maxz)):
			inZone = 1
	if inZone:
		return True
	else:
		return False

# отметить попадание MatchCount
def updateMatchCount(value, dictKey, arr):
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
			# заполняем зоны входа userzones
			for user in s['userzones']:
				for uzone in user['uzones']:
					for izone in uzone['IncomeZones']:
						vertices = izone['vertices']
						vector = [(x, y)]
						minz = izone['minz']
						maxz = izone['maxz']
						match = inPolygon(vertices, vector)
						if (match and inInterval(z, minz, maxz)):
							# проверяем наличие id в IncomeZones
							if not dictKeyInArray(izone['id'], 'id', obj['IncomeZones'], 0):
								# записываем id в словарь
								obj['IncomeZones'].append({'id': izone['id'], 'cron': 0})
							else:
								dictKeyInArray(izone['id'], 'id', obj['IncomeZones'], 1)
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
		set_interval(lightUpTagBelongTo, 1)
		set_interval(lightUpTagBelongToUzone, 1)

# подсвечиваем принадлежность метки, если запрос пользователя
def lightUpTagBelongTo():
	for a in active_users:
		if 'belong' in a:
			tag_id = a['belong']['tag_id']
			for i in unique:
				if i['tag_id'] == tag_id:
					if 'location' in i:
						if not 'id' in a['belong']:
							a['belong']['type'] = i['location']['type']
							a['belong']['id'] = i['location']['id']
							sendToUserElemForLightUp(i['location']['type'], i['location']['id'], a['id'])
						elif a['belong']['id'] != i['location']['id']:
							a['belong']['type'] = i['location']['type']
							a['belong']['id'] = i['location']['id']
							sendToUserElemForLightUp(i['location']['type'], i['location']['id'], a['id'])

# подсвечиваем принадлежность метки зоне пользователя, если запрос пользователя
def lightUpTagBelongToUzone():
	for a in active_users:
		if 'belonguzone' in a:
			tag_id = a['belonguzone']['tag_id']
			if not 'type' in a['belonguzone']:
				a['belonguzone']['type'] = '' 
			for i in unique:
				if i['tag_id'] == tag_id:
					for user in i['userzone']:
						if user['user_id'] == a['id']:
							if user['UserZoneLocation']['type'] == 'inuzone':
								if not 'id' in a['belonguzone']:
									a['belonguzone']['id'] = user['UserZoneLocation']['id']
									a['belonguzone']['type'] = user['UserZoneLocation']['type']
									sendToUserUzoneForLightUp('inuzone', \
										 user['UserZoneLocation']['id'], a['id'], i['zone_id'])
								elif a['belonguzone']['id'] != user['UserZoneLocation']['id']:
									a['belonguzone']['id'] = user['UserZoneLocation']['id']
									a['belonguzone']['type'] = user['UserZoneLocation']['type']
									sendToUserUzoneForLightUp('inuzone', \
										 user['UserZoneLocation']['id'], a['id'], i['zone_id'])
							elif user['UserZoneLocation']['type'] == 'outofzone' \
							 and a['belonguzone']['type'] == 'inuzone':
							 	a['belonguzone']['type'] = 'outofzone'
							 	a['belonguzone']['id'] = 0
							 	sendToUserUzoneForLightUp('outofzone', 0, a['id'], i['zone_id'])

def sendToUserElemForLightUp(elemtype, elemid, user_id):
	#определение dae_name и рассылка пользователю для подсветки
	if elemtype == 'floor':
		fid = elemid
		dae = Floor.objects.get(id=fid)
		dae_name = dae.dae_FloorName
		dae_id = dae.id
		vertices = list(VerticesFloor.objects.filter(Floor_id=dae_id).values('x', 'y'))
		service_queue('show_location', json({'user': user_id, 'data': {'type': \
			'floor', 'location': dae_name, 'vertices': json(vertices)}}))
	elif elemtype == 'kabinet':
		kid = elemid
		dae = Kabinet_n_Outer.objects.get(id=kid)
		dae_name = dae.dae_Kabinet_n_OuterName
		dae_id = dae.id
		vertices = list(VerticesKabinet_n_Outer.objects.filter(Kabinet_n_Outer_id=dae_id).values('x', \
		 'y'))
		service_queue('show_location', json({'user': user_id, 'data': {'type': \
			'kabinet', 'location': dae_name, 'vertices': json(vertices)}}))

def sendToUserUzoneForLightUp(elemtype, elemid, user_id, landscape_id):
	if elemid != 0:
		uzoneid = elemid
		vertices = list(VerticesUserZone.objects.filter(UserZone_id=elemid).values('xCoord', 'yCoord', 'zmin'))
		vxy = []
		zmin = vertices[0]['zmin']
		for v in vertices:
			vxy.append([v['xCoord'], v['yCoord']])
		service_queue('show_location', json({'user': user_id, 'data': {'type': elemtype, \
		 'vertices': vxy, 'faces': getFacesFromVert(vertices), 'id': elemid, 'zmin': zmin, \
		  'landscape_id': landscape_id}}))
	elif elemid == 0:
		service_queue('show_location', json({'user': user_id, 'data': {'type': elemtype, \
			'vertices':0, 'id': 0}}))
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
		# second and other lines
		else:
			line = line[0].split('\r\n')
			for i in line:
				line = i.split(',')
				if len(line) > 0 and len(line) > 4:
					dictionary = {'tag_id':line[3], 'x': float(line[4]), 'y': float(line[5]), 'z': float(line[6]), 'zone':line[8], 'zone_id': line[11]}
					#наполняем unique
					doubled = 0
					for i in unique:
						if i['tag_id'] == line[3]:
							i['xNew'] = dictionary['x']
							i['yNew'] = dictionary['y']
							i['zNew'] = dictionary['z']
							i['time'] = dictionary['zone']
							i['zone_id'] = dictionary['zone_id']
							i['cron'] = 0
							#быстрая корректировка
							correctFast(i)
							doubled = 1
					if not(doubled):
						try:
							t = Tag.objects.get(TagId=dictionary['tag_id'])
							TurnOnOffTag(Tag_id=t.TagId, OnOff=1, OnOffTime=datetime.datetime.now(), \
								LoadLandscape_id=dictionary['zone_id']).save()
						except:
							pass
						updateUnique(dictionary, 'add')
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
		# for i in active_users:
		# 	try:
		# 		if len(i['data']) > 0:
		# 			service_queue('coords_lock', json({'user': i['id'],'data': i['data']}))
		# 			i['data'] = []
		# 	except:
		# 		pass	
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
	a = request.get_host().split(':')
	args['hostname'] = a[0]
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
	a = request.get_host().split(':')
	args['hostname'] = a[0]
	args['unique'] = []
	for i in unique:
		if i['zone_id'] == landscape_id:
			args['unique'].append(i)
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
	# отправить на сервер сессию
	if request.method == 'POST':
		string = simplejson.loads(request.body)
		url = 'http://192.168.1.111:8000'
		headers = {'content-type:': 'application/json', 'charset': 'utf-8'}
		if string['method'] == 'sendsession':
			data = json(string['data'])
			try:
				r = requests.post(url, data=data, headers=headers)
				json_data = simplejson.loads(r.text)
			except:
				json_data = 'ответа нет'
			args['message'] = json_data
			a = render_to_string('notification.html', args)
			return JsonResponse({'string': json_data})
		if string['method'] == 'getsessionlist':
			data = json({'command':"getListSessions"})
			try:
				r = request.post(url, data=data, headers=headers)
				json_data = simplejson.loads(r.text)
			except:
				json_data = 'ответа нет'
			args['message'] = json_data
			a = render_to_string('notification.html', args)
			return JsonResponse({'string': json_data})
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
				i['maxz'] = strmax['z']
				i['minz'] = strmin['z']
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

def getUzonesWithoutGroups(uzones, uzonegroupuzones, user_id):
	arr = []
	for u in uzones:
		match = 0
		for guz in uzonegroupuzones:
			if u.id == guz.UserZone_id:
				match = 1
		if not match and u.User_id==user_id:
			arr.append(u)
	return arr

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
	args['uzones'] = UserZone.objects.filter(LoadLandscape_id=landscape_id, \
	 User_id=auth.get_user(request).id)
	args['uzonegroups'] = GroupUserZone.objects.filter(User_id=auth.get_user(request).id, \
	 LoadLandscape_id=landscape_id)
	args['uzonegroupuzones'] = GroupUserZoneUserZone.objects.all()
	args['uzoneswithoutgroups'] = getUzonesWithoutGroups(args['uzones'], args['uzonegroupuzones'], \
	 auth.get_user(request).id)
	args['izoneuzone'] = IncomeZoneUserZone.objects.all()
	args['ezoneuzone'] = ExcludeZoneUserZone.objects.all()
	args['vzones'] = VerticesIncomeZone.objects.all()
	args['evzones'] = VerticesExcludeZone.objects.all()
	args['uvzones'] = VerticesUserZone.objects.all()
	args['lUserZone'] = LoadLandscapeUserZone.objects.all()
	args['bIncomeZone'] = BuildingIncomeZone.objects.all()
	args['bExcludeZone'] =  BuildingExcludeZone.objects.all()
	args['bUserZone'] = BuildingUserZone.objects.all()
	args['fIncomeZone'] = FloorIncomeZone.objects.all()
	args['fExcludeZone'] = FloorExcludeZone.objects.all()
	args['fUserZone'] = FloorUserZone.objects.all()
	args['kIncomeZone'] = KabinetIncomeZone.objects.all()
	args['kExcludeZone'] = KabinetExcludeZone.objects.all()
	args['kUserZone'] = KabinetUserZone.objects.all()
	args['objecttype'] = ObjectType.objects.all()
	args['objects'] = Object.objects.all()
	args['objectobjecttypes'] = ObjectObjectType.objects.all().values('ObjectType_id', \
		 'Object_id', 'ObjectType__Name')
	args['objectbuilding'] = ObjectBuilding.objects.all().values('Building_id', \
				 'Object_id', 'Building__dae_BuildingName')
	args['objectfloor'] = ObjectFloor.objects.all().values('Floor_id', 'Object_id', \
	 'Floor__dae_FloorName', 'Floor__Building_id')
	args['objectkabinet'] = ObjectKabinet.objects.all().values('Kabinet_id', 'Object_id', \
		 'Kabinet__dae_Kabinet_n_OuterName', 'Kabinet__Floor_id')
	args['objecttable'] = render_to_string('objecttable.html', args)
	if request.method == 'POST':
		string = simplejson.loads(request.body)
		landscape_id = string['landscape_id']
		# проверка на hex
		if string['method'] == 'checkhex':
			string = string['string']
			try:
				int(string, 16)
				error = 0
				text = 0
			except:
				error = 1
				text = "Введенное значение не соответствует hex."
			return JsonResponse({'error': error, 'text': text })
		# привязать конекретный объект к статике
		if string['method'] == 'linkobjecttostatic':
			static_id = string['static_id']
			static_type = string['static_type']
			obj_id = string['obj_id']
			ObjectBuilding.objects.filter(Object_id=obj_id).delete()
			ObjectFloor.objects.filter(Object_id=obj_id).delete()
			ObjectKabinet.objects.filter(Kabinet_id=obj_id).delete()
			if static_type == 'building':
				ObjectBuilding.objects.create(Building_id=static_id, Object_id=obj_id)
			elif static_type == 'floor':
				ObjectFloor.objects.create(Floor_id=static_id, Object_id=obj_id)
			elif static_type == 'kabinet':
				ObjectKabinet.objects.create(Kabinet_id=static_id, Object_id=obj_id)
			args['objectbuilding'] = ObjectBuilding.objects.all()
			args['objectfloor'] = ObjectFloor.objects.all()
			args['objectkabinet'] = ObjectKabinet.objects.all()
			args['objecttable'] = render_to_string('objecttable.html', args)
			return JsonResponse({'string': args['objecttable']})
		# отправить конкретный объект на сервер "Команда Обновить"
		if string['method'] == 'sendobjectupdatetoserver':
			obj_id = string['obj_id']
			obj = ObjectObjectType.objects.filter(Object_id=obj_id).values('Object__id', \
					 'Object__Name', 'Object__Description', 'Object__xCoord', 'Object__yCoord', \
					  'Object__zCoord', 'Object__server_id', 'Object__server_inUse', \
					   'Object__server_minNumPoints', 'Object__server_radius', 'Object__server_type', \
					   'ObjectType_id')
			data = {}
			obj_type = ObjectType.objects.get(id=obj[0]['ObjectType_id'])
			id_layer = LoadLandscape.objects.get(landscape_id=landscape_id).server_id
			data['command'] = obj_type.CommandUpdate
			if obj_type.id == 1:
				data['masterAnchors'] = []
				for i in obj:
					data['masterAnchors'].append({'id': i['Object__server_id'], 'name': i['Object__Name'], \
						 'description': i['Object__Description'], 'x': i['Object__zCoord'], \
						 'y': i['Object__xCoord'], 'z': i['Object__yCoord'], \
						  'inUse': bool(i['Object__server_inUse']), \
						  'idLayer': id_layer})
			elif obj_type.id == 2:
				data['anchors'] = []
				for i in obj:
					data['anchors'].append({'id': i['Object__server_id'], 'name': i['Object__Name'], \
						 'description': i['Object__Description'], 'x': i['Object__zCoord'], \
						  'y': i['Object__xCoord'], 'z': i['Object__yCoord'], \
						   'inUse': bool(i['Object__server_inUse']), \
						    'idLayer': id_layer, 'type': i['Object__server_type'], \
						    'radius': i['Object__server_radius'], \
						     'minNumPoints': i['Object__server_minNumPoints']})
			url = 'http://192.168.1.111:8000'
			data = json(data)
			headers = {'content-type:': 'application/json', 'charset': 'utf-8'}
			r = requests.post(url, data=data, headers=headers)
			json_data = simplejson.loads(r.text)
			return JsonResponse({'string': data})

		# отправить конкретный объект на сервер "команда Добавить"
		if string['method'] == 'sendobjecttoserver':
			obj_id = string['obj_id']
			obj = ObjectObjectType.objects.filter(Object_id=obj_id).values('Object__id', \
					 'Object__Name', 'Object__Description', 'Object__xCoord', 'Object__yCoord', \
					  'Object__zCoord', 'Object__server_id', 'Object__server_inUse', \
					   'Object__server_minNumPoints', 'Object__server_radius', 'Object__server_type', \
					   'ObjectType_id')
			data = {}
			obj_type = ObjectType.objects.get(id=obj[0]['ObjectType_id'])
			id_layer = LoadLandscape.objects.get(landscape_id=landscape_id).server_id
			data['command'] = obj_type.Command
			if obj_type.id == 1:
				data['masterAnchors'] = []
				for i in obj:
					data['masterAnchors'].append({'id': i['Object__server_id'], 'name': i['Object__Name'], \
						 'description': i['Object__Description'], 'x': i['Object__zCoord'], \
						 'y': i['Object__xCoord'], 'z': i['Object__yCoord'], \
						  'inUse': bool(i['Object__server_inUse']), \
						  'idLayer': id_layer})
			elif obj_type.id == 2:
				data['anchors'] = []
				for i in obj:
					data['anchors'].append({'id': i['Object__server_id'], 'name': i['Object__Name'], \
						 'description': i['Object__Description'], 'x': i['Object__zCoord'], \
						  'y': i['Object__xCoord'], 'z': i['Object__yCoord'], \
						   'inUse': bool(i['Object__server_inUse']), \
						    'idLayer': id_layer, 'type': i['Object__server_type'], \
						    'radius': i['Object__server_radius'], \
						     'minNumPoints': i['Object__server_minNumPoints']})
			url = 'http://192.168.1.111:8000'
			data = json(data)
			headers = {'content-type:': 'application/json', 'charset': 'utf-8'}
			r = requests.post(url, data=data, headers=headers)
			json_data = simplejson.loads(r.text)
			return JsonResponse({'string': data})


		# отправить objecttype на сервер
		if string['method'] == 'sendobjectstypetoserver':
			obj_type = string['obj_type']
			objecttype = ObjectType.objects.get(id=obj_type)
			data = {}
			data['command'] = objecttype.Command
			obj = ObjectObjectType.objects.filter(ObjectType_id=objecttype.id).values('Object__id', \
					 'Object__Name', 'Object__Description', 'Object__xCoord', 'Object__yCoord', \
					  'Object__zCoord', 'Object__server_id', 'Object__server_inUse', \
					   'Object__server_minNumPoints', 'Object__server_radius', 'Object__server_type')
			if obj_type == 1:
				data['masterAnchors'] = []
				for i in obj:
					data['masterAnchors'].append({'id': i['Object__server_id'], 'name': i['Object__Name'], \
						 'description': i['Object__Description'], 'x': i['Object__zCoord'], \
						 'y': i['Object__xCoord'], 'z': i['Object__yCoord'], \
						  'inUse': bool(i['Object__server_inUse']), \
						  'idLayer': int(landscape_id)})
			elif obj_type == 2:
				data['anchors'] = []
				for i in obj:
					data['anchors'].append({'id': i['Object__server_id'], 'name': i['Object__Name'], \
						 'description': i['Object__Description'], 'x': i['Object__zCoord'], \
						  'y': i['Object__xCoord'], 'z': i['Object__yCoord'], \
						   'inUse': bool(i['Object__server_inUse']), \
						    'idLayer': int(landscape_id), 'type': i['Object__server_type'], \
						    'radius': i['Object__server_radius'], \
						     'minNumPoints': i['Object__server_minNumPoints']})
			url = 'http://192.168.1.111:8000'
			data = json(data)
			headers = {'content-type:': 'application/json', 'charset': 'utf-8'}
			r = requests.post(url, data=data, headers=headers)
			json_data = simplejson.loads(r.text)
			return JsonResponse({'string': json_data})
		# сохранить параметры объекта
		if string['method'] == 'saveparameters':
			objecttype_id = string['objecttype_id']
			obj_id = string['obj_id']
			Name = string['name']
			server_id = string['server_id']
			Description = string['description']
			server_inUse = string['server_inUse']
			if objecttype_id == 1:
				Object.objects.filter(id=obj_id).update(Name=Name, server_id=server_id, \
				 Description=Description, server_inUse=server_inUse)
			elif objecttype_id == 2:
				server_type = string['server_type']
				server_radius = string['server_radius']
				server_minNumPoints = string['server_minNumPoints']
				Object.objects.filter(id=obj_id).update(Name=Name, server_id=server_id, \
					Description=Description, server_inUse=server_inUse, server_type=server_type, \
					 server_radius=server_radius, server_minNumPoints=server_minNumPoints)
			args['objects'] = Object.objects.all()
			args['objecttable'] = render_to_string('objecttable.html', args)
			return JsonResponse({'string': args['objecttable']})
		# показать информацию о конкретном объект
		if string['method'] == 'getobjectinfo':
			args['objecttype'] = ObjectType.objects.all()
			obj_id = string['obj_id']
			obj_type = string['obj_type']
			args['objectobjecttype'] = ObjectObjectType.objects.get(Object_id=obj_id)
			args['obj'] = Object.objects.get(id=obj_id)
			args['obj_type'] = ObjectType.objects.get(id=obj_type)
			args['getobjectinfo'] = render_to_string('getobjectinfo.html', args)
			return JsonResponse({'string': args['getobjectinfo']})
		# показать конкретный объект
		if string['method'] == 'showobject':
			obj_id = string['obj_id']
			a = Object.objects.get(id=obj_id)
			return JsonResponse({'string': {'id': a.id, 'x': a.xCoord, 'y': a.yCoord, 'z': a.zCoord}})
		# показать все объекты
		if string['method'] == 'showallobjects':
			landscape_id = string['landscape_id']
			objecttype_id = string['objecttype_id']
			meshes = []
			objType = Object.objects.filter(objectobjecttype__ObjectType_id=objecttype_id, \
			 LoadLandscape_id=landscape_id).values('id', \
			 'Name', 'xCoord', 'yCoord', 'zCoord', \
			  'objectobjecttype__ObjectType_id', 'server_id', 'server_inUse', 'server_type', \
			   'server_radius', 'server_minNumPoints')
			for i in objType:
				meshes.append(i)
			return JsonResponse({'string':meshes})
		# показать только привязанные объекты building
		if string['method'] == 'showlinkedobjectsbuilding':
			landscape_id = string['landscape_id']
			objecttype_id = string['objecttype_id']
			static_name = string['static_name']
			meshes = []
			for b in args['buildings']:
				if b.dae_BuildingName == static_name:
					bid = b.id
					break
			obj = Object.objects.filter(objectobjecttype__ObjectType_id=objecttype_id, \
				LoadLandscape_id=landscape_id).values('id', \
			 'Name', 'xCoord', 'yCoord', 'zCoord', \
			  'objectobjecttype__ObjectType_id', 'server_id', 'server_inUse', 'server_type', \
			   'server_radius', 'server_minNumPoints')
			for o in obj:
				for b in args['objectbuilding']:
					if o['id'] == b['Object_id'] and b['Building__dae_BuildingName'] == static_name:
						meshes.append(o)
						break
				fid = []
				for f in args['floors']:
					if f.Building_id == bid:
						fid.append(f.id)
				for f in args['objectfloor']:
					if o['id'] == f['Object_id'] and f['Floor__Building_id'] == bid:
						fid.append(f['Floor_id'])
						meshes.append(o)
						break
				for k in args['objectkabinet']:
					if o['id'] == k['Object_id']:
						for f in fid:
							if k['Kabinet__Floor_id'] == f:
								meshes.append(o)
								break
			return JsonResponse({'string':meshes})
		# показывать только привязанные объекты floor
		if string['method'] == 'showlinkedobjectsfloor':
			landscape_id = string['landscape_id']
			objecttype_id = string['objecttype_id']
			static_name = string['static_name']
			meshes = []
			obj = Object.objects.filter(objectobjecttype__ObjectType_id=objecttype_id, \
				LoadLandscape_id=landscape_id).values('id', \
			 'Name', 'xCoord', 'yCoord', 'zCoord', \
			  'objectobjecttype__ObjectType_id', 'server_id', 'server_inUse', 'server_type', \
			   'server_radius', 'server_minNumPoints')
			for f in args['floors']:
				if f.dae_FloorName == static_name:
					fid = f.id
			for o in obj:
				for f in args['objectfloor']:
					if o['id'] == f['Object_id'] and f['Floor__dae_FloorName'] == static_name:
						meshes.append(o)
						break
				for k in args['objectkabinet']:
					if o['id'] == k['Object_id']:
						if k['Kabinet__Floor_id'] == fid:
							meshes.append(o)
							break
			return JsonResponse({'string': meshes})
		# показывать только привязанные объекты kabinet
		if string['method'] == 'showlinkedobjectskabinet':
			landscape_id = string['landscape_id']
			objecttype_id = string['objecttype_id']
			static_name = string['static_name']
			meshes = []
			obj = Object.objects.filter(objectobjecttype__ObjectType_id=objecttype_id, \
				LoadLandscape_id=landscape_id).values('id', \
			 'Name', 'xCoord', 'yCoord', 'zCoord', \
			  'objectobjecttype__ObjectType_id', 'server_id', 'server_inUse', 'server_type', \
			   'server_radius', 'server_minNumPoints')
			for o in obj:
				for k in args['objectkabinet']:
					if o['id'] == k['Object_id'] and k['Kabinet__dae_Kabinet_n_OuterName'] == static_name:
						meshes.append(o)
						break
			return JsonResponse({'string': meshes})
		#изменить координаты
		if string['method'] == 'changecoords':
			Object.objects.filter(id=string['obj']).update(xCoord=string['xCoord'], \
			 yCoord=string['yCoord'], zCoord=string['zCoord'])
			args['objects'] = Object.objects.all()
			args['objecttable'] = render_to_string('objecttable.html', args)
			return JsonResponse({'string': args['objecttable']})
		# удалить объект objectdelete
		if string['method'] == 'objectdelete':
			obj_id = string['obj_id']
			a = Object.objects.filter(id=obj_id)
			objectobjecttype = ObjectObjectType.objects.get(Object_id=obj_id)
			obj_type = ObjectType.objects.get(id=objectobjecttype.ObjectType_id)
			# отправить на сервер комманду
			data = {}
			data['command'] = obj_type.CommandDelete
			data[obj_type.Name_eng] = []
			if obj_type.id == 1:
				data[obj_type.Name_eng].append({'id': a[0].server_id})
			elif obj_type.id == 2:
				data[obj_type.Name_eng].append({'id': a[0].server_id})
			url = 'http://192.168.1.111:8000'
			data = json(data)
			headers = {'content-type:': 'application/json', 'charset': 'utf-8'}
			try:
				r = requests.post(url, data=data, headers=headers)
				json_data = simplejson.loads(r.text)
				args['success'] = 'Команда успешно направлена на сервер'
			except:
				args['error'] = 'Сервер позиционирования не отвечает.'
			a.delete()
			args['objects'] = Object.objects.all()
			args['objecttable'] = render_to_string('objecttable.html', args)
			# отправить запрос на сервер
			return JsonResponse({'string': args['objecttable']})
		#подcветить выбранный objecttype in objecttable
		if string['method'] == 'coloredobjects':
			args['coloredobjects'] = ObjectObjectType.objects.filter(ObjectType_id=string['objecttype'])
			args['objecttable'] = render_to_string('objecttable.html', args)
			return JsonResponse({'string': args['objecttable']})
		#добавить объект
		if string['method'] == 'addobject':
			point = string['point']
			objecttype = string['objecttype']
			a = Object.objects.create(xCoord=point['x'], yCoord=point['y'], zCoord=0, \
			 LoadLandscape_id=args['landscape_id'])
			ObjectObjectType.objects.create(Object_id=a.id, ObjectType_id=objecttype)
			args['objects'] = Object.objects.filter(LoadLandscape_id=args['landscape_id'])
			args['objectobjecttypes'] = ObjectObjectType.objects.all().values('ObjectType_id', \
			 'Object_id', 'ObjectType__Name')
			args['objecttable'] = render_to_string('objecttable.html', args)
			return JsonResponse({'string': args['objecttable']})
		#изменить тип объекта
		if string['method'] == 'typechange':
			objecttype = string['objecttype']
			obj = string['object']
			if len(ObjectObjectType.objects.filter(Object_id=obj)) > 0:
				ObjectObjectType.objects.filter(Object_id=obj).update(ObjectType_id=objecttype)
			else:
				ObjectObjectType.objects.create(Object_id=obj, ObjectType_id=objecttype)
			args['objectobjecttypes'] = ObjectObjectType.objects.all().values('ObjectType_id', \
			 'Object_id', 'ObjectType__Name')
			args['objecttable'] = render_to_string('objecttable.html', args)
			return JsonResponse({'string': args['objecttable']})
		#изменить имя объекта
		if string['method'] == 'changename':
			obj = string['object']
			name = string['name']
			Object.objects.filter(id=obj).update(Name=name)
			args['objects'] = Object.objects.filter(LoadLandscape_id=args['landscape_id'])
			args['objecttable'] = render_to_string('objecttable.html', args)
			return JsonResponse({'string': args['objecttable']})
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
		#добавить зону пользователя
		if string['method'] == 'adduzone':
			user_id = string['user_id']
			zone = UserZone.objects.create(User_id=user_id, LoadLandscape_id=landscape_id)
			for i in string['vertices']:
				VerticesUserZone.objects.create(xCoord=i['x'], yCoord=i['y'], \
					UserZone_id=zone.id)
			args['uzones'] = UserZone.objects.filter(User_id=user_id, LoadLandscape_id=landscape_id)
			args['data'] = {}
			args['data']['userzonetable'] = render_to_string('userzonetable.html', args)
			#обновляем информацию в списке групп
			args['uzoneswithoutgroups'] = getUzonesWithoutGroups(args['uzones'], \
			 args['uzonegroupuzones'], auth.get_user(request).id)
			args['data']['uzonegrouptable'] = render_to_string('userzonegrouptable.html', args)
			args['uzonegroupuzones'] = GroupUserZoneUserZone.objects.all()
			#обновляем информацию в incomezone
			args['data']['zonetable'] = render_to_string('incomezonetable.html', args)
			#обновляем информацию в excludezone
			args['data']['excludezonetable'] = render_to_string('excludezonetable.html', args)
			return JsonResponse(args['data']) 
		#добавить зону пользователя в группу зон пользователя
		if string['method'] == 'adduzonetogroup':
			uzoneid = string['uzoneid']
			groupid = string['groupid']
			GroupUserZoneUserZone.objects.create(GroupUserZone_id=groupid, \
				 UserZone_id=uzoneid)
			args['uzonegroupuzones'] = GroupUserZoneUserZone.objects.all()
			args['uzoneswithoutgroups'] = getUzonesWithoutGroups(args['uzones'], \
			 args['uzonegroupuzones'], auth.get_user(request).id)
			args['colored'] = GroupUserZoneUserZone.objects.filter(GroupUserZone_id= \
				groupid).values('UserZone__id')
			args['data'] = {}
			args['data']['uzonegrouptable'] = render_to_string('userzonegrouptable.html', args)
			args['data']['userzonetable'] = render_to_string('userzonetable.html', args)
			return JsonResponse(args['data'])
		#удалить зону пользователя из группы зон пользователя
		if string['method'] == 'removeuzonetogroup':
			uzoneid = string['uzoneid']
			groupid = string['groupid']
			GroupUserZoneUserZone.objects.filter(GroupUserZone_id=groupid, \
				 UserZone_id=uzoneid).delete()
			args['uzonegroupuzones'] = GroupUserZoneUserZone.objects.all()
			args['uzoneswithoutgroups'] = getUzonesWithoutGroups(args['uzones'], \
			 args['uzonegroupuzones'], auth.get_user(request).id)
			args['colored'] = GroupUserZoneUserZone.objects.filter(GroupUserZone_id= \
				groupid).values('UserZone__id')
			args['data'] = {}
			args['data']['uzonegrouptable'] = render_to_string('userzonegrouptable.html', args)
			args['data']['userzonetable'] = render_to_string('userzonetable.html', args)
			return JsonResponse(args['data'])
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
		#удалить зону пользователя
		if string['method'] == 'delete_userzone':
			zoneid = string['zoneid']
			UserZone.objects.filter(id=zoneid).delete()
			args['uzones'] = UserZone.objects.filter(LoadLandscape_id=landscape_id, \
			 User_id=auth.get_user(request).id)
			args['data'] = {}
			args['data']['userzonetable'] = render_to_string('userzonetable.html', args)
			#обновляем информацию в списке групп
			args['uzoneswithoutgroups'] = getUzonesWithoutGroups(args['uzones'], \
			 args['uzonegroupuzones'], auth.get_user(request).id)
			args['data']['uzonegrouptable'] = render_to_string('userzonegrouptable.html', args)
			#Обновляем информацию includezones
			args['data']['zonetable'] = render_to_string('incomezonetable.html', args)
			#Обновляем информацию excludezones
			args['data']['excludezonetable'] = render_to_string('excludezonetable.html', args)
			return JsonResponse(args['data'])
		# переименовать зону пользователя
		if string['method'] == 'rename_userzone':
			zoneid = string['zoneid']
			name = string['name']
			UserZone.objects.filter(id=zoneid).update(UserZoneName=name)
			args['uzones'] = UserZone.objects.filter(LoadLandscape_id=landscape_id, \
			 User_id=auth.get_user(request).id)
			args['data'] = {}
			args['data']['userzonetable'] = render_to_string('userzonetable.html', args)
			#обновляем информацию в списке групп
			args['uzoneswithoutgroups'] = getUzonesWithoutGroups(args['uzones'], \
			 args['uzonegroupuzones'], auth.get_user(request).id)
			args['data']['uzonegrouptable'] = render_to_string('userzonegrouptable.html', args)
			args['data']['zonetable'] = render_to_string('incomezonetable.html', args)
			args['data']['excludezonetable'] = render_to_string('excludezonetable.html', args)
			return JsonResponse(args['data'])
		# переименовать группу зон пользователя
		if string['method'] == 'renamezonegroup':
			groupid = string['groupid']
			groupname = string['groupname']
			GroupUserZone.objects.filter(id=groupid, LoadLandscape_id=string['landscape_id']).update(GroupName=groupname)
			args['uzonegroups'] = \
			 GroupUserZone.objects.filter(User_id=auth.get_user(request).id, LoadLandscape_id=string['landscape_id'])
			args['data'] = {}
			args['data']['uzonegrouptable'] = render_to_string('userzonegrouptable.html', args)
			return JsonResponse(args['data'])
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
		# привязать зону входа к зоне пользователя(incomezone to userzone)
		if string['method'] == 'linkincomezonetouserzone':
			izone = string['izone']
			uzone = string['uzone']
			delZones(izone, 'income')
			IncomeZoneUserZone.objects.filter(IncomeZone_id=izone, UserZone_id=uzone).delete()
			IncomeZoneUserZone.objects.create(IncomeZone_id=izone, UserZone_id=uzone)
			# обновляем высоты зон входа до пользовательских зон
			borders = VerticesUserZone.objects.filter(UserZone_id=uzone)[0]
			zminUzone = borders.zmin
			zmaxUzone = borders.zmax
			VerticesIncomeZone.objects.filter(IncomeZone_id=izone).update(zmax=zmaxUzone, zmin=zminUzone)
			args['izoneuzone'] = IncomeZoneUserZone.objects.all()
			args['data'] = {}
			args['data']['zonetable'] = render_to_string('incomezonetable.html', args)
			return JsonResponse(args['data'])
		# привязать зону исключения к зоне пользователя(excludezone to userzone)
		if string['method'] == 'linkexcludezonetouserzone':
			ezone = string['ezone']
			uzone = string['uzone']
			delZones(ezone, 'exclude')
			ExcludeZoneUserZone.objects.filter(ExcludeZone_id=ezone, UserZone_id=uzone).delete()
			ExcludeZoneUserZone.objects.create(ExcludeZone_id=ezone, UserZone_id=uzone)
			# обновляем высоты зон исключения до пользовательских зон
			borders = VerticesUserZone.objects.filter(UserZone_id=uzone)[0]
			zminUzone = borders.zmin
			zmaxUzone = borders.zmax
			VerticesExcludeZone.objects.filter(ExcludeZone_id=ezone).update(zmax=zmaxUzone, zmin=zminUzone)
			args['ezoneuzone'] = ExcludeZoneUserZone.objects.all()
			args['data'] = {}
			args['data']['excludezonetable'] = render_to_string('excludezonetable.html', args)
			return JsonResponse(args['data'])
		# отвязать зону входа от зоны пользователя(incomezone to userzone)
		if string['method'] == 'unlinkincomezonetouserzone':
			izuz = string['izuz']
			IncomeZoneUserZone.objects.filter(id=izuz).delete()
			args['izoneuzone'] = IncomeZoneUserZone.objects.all()
			args['data'] = {}
			args['data']['zonetable'] = render_to_string('incomezonetable.html', args)
			return JsonResponse(args['data'])
		# отвязать зону исключения от зоны пользователя(excludezone to userzone)
		if string['method'] == 'unlinkexcludezonetouserzone':
			ezuz = string['ezuz']
			ExcludeZoneUserZone.objects.filter(id=ezuz).delete()
			args['ezoneuzone'] = ExcludeZoneUserZone.objects.all()
			args['data'] = {}
			args['data']['excludezonetable'] = render_to_string('excludezonetable.html', args)
			return JsonResponse(args['data'])
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
		# привязать зону пользователя
		if string['method'] == 'link_uzone':
			zoneid = string['zoneid']
			if string['type'] == 'landscape':
				lid = string['id']
				l = LoadLandscape.objects.get(landscape_id=landscape_id)
				zmin = 0
				zmax = 3
				# устанавливаем z для зоны по привязанномуэлементу
				VerticesUserZone.objects.filter(UserZone_id=zoneid).update(zmin=zmin, \
				 zmax=zmax)
				# удаляем ранние привязки
				delZones(zoneid, 'uzones')
				# сцепляем зону с объектом
				LoadLandscapeUserZone.objects.create(LoadLandscape_id=landscape_id, UserZone_id=zoneid)
			if string['type'] == 'building':
				bid = string['id']
				b = Building.objects.get(id=bid)
				zmin = b.minz
				zmax = b.maxz
				# устанавливаем z для зоны по привязанномуэлементу
				VerticesUserZone.objects.filter(UserZone_id=zoneid).update(zmin=zmin, \
				 zmax=zmax)
				# удаляем ранние привязки
				delZones(zoneid, 'uzones')
				# сцепляем зону с объектом
				BuildingUserZone.objects.create(Building_id=bid, UserZone_id=zoneid)
			elif string['type'] == 'floor':
				fid = string['id']
				f = Floor.objects.get(id=fid)
				zmin = f.minz
				zmax = f.maxz
				# устанавливаем z для зоны по привязанномуэлементу
				VerticesUserZone.objects.filter(UserZone_id=zoneid).update(zmin=zmin, \
					zmax=zmax)
				# удаляем ранние привязки
				delZones(zoneid, 'uzones')
				# сцепляем зону с объектом
				FloorUserZone.objects.create(Floor_id=fid, UserZone_id=zoneid)
			elif string['type'] == 'kabinet':
				kid = string['id']
				k = Kabinet_n_Outer.objects.get(id=kid)
				zmin = k.minz
				zmax = k.maxz
				# устанавливаем z для зоны по привязанномуэлементу
				VerticesUserZone.objects.filter(UserZone_id=zoneid).update(zmin=zmin, \
				 zmax=zmax)
				# удаляем ранние привязки
				delZones(zoneid, 'uzones')
				# сцепляем зону с объектом
				KabinetUserZone.objects.create(Kabinet_id=kid, UserZone_id=zoneid)
			args['uzones'] = UserZone.objects.filter(LoadLandscape_id=landscape_id, \
			 User_id=auth.get_user(request).id)
			return render(request, 'userzonetable.html', args)
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
		# отыепить userzone
		if string['method'] == 'unlink_uzone':
			zoneid = string['zoneid']
			delZones(zoneid, 'uzones')
			args['uzones'] =UserZone.objects.filter(LoadLandscape_id=landscape_id, \
				 User_id=auth.get_user(request).id)
			return render(request, 'userzonetable.html', args)
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
		# сохраняем максимальные или минимальные значения высоты зоны userzone
		if string['method'] == 'savemin_uzone':
			zoneid = string['zoneid']
			value = string['value']
			VerticesUserZone.objects.filter(UserZone_id=zoneid).update(zmin=value)
			args['uzones'] = UserZone.objects.filter(LoadLandscape_id=landscape_id, \
				 User_id=auth.get_user(request).id)
			return render(request, 'userzonetable.html', args)
		if string['method'] == 'savemax_uzone':
			zoneid = string['zoneid']
			value = string['value']
			VerticesUserZone.objects.filter(UserZone_id=zoneid).update(zmax=value)
			args['uzones'] = UserZone.objects.filter(LoadLandscape_id=landscape_id, \
				User_id=auth.get_user(request).id)
			return render(request, 'userzonetable.html', args)
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
			return render(request, 'incomezonetable.html', args)
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
		# возвращаем зоны, привязанные к объекту, чтобы их окрасить в таблице userzone
		if string['method'] == 'colored_uzone':
			ugrzoneid = string['ugrzoneid']
			args['colored'] = GroupUserZoneUserZone.objects.filter(GroupUserZone_id= \
				ugrzoneid).values('UserZone__id')
			mesh = []
			for i in args['colored']:
				mesh.append({'id': i['UserZone__id'], 'vertices': [], 'izones': [], 'ezones': []})
			# записываем вершины для отображения зон группы
			for i in VerticesUserZone.objects.all():
				for j in mesh:
					if i.UserZone_id == j['id']:
						j['vertices'].append({'x': i.xCoord, 'y': i.yCoord, 'zmin': i.zmin, \
						 'zmax': i.zmax})
			# записывем поверхности для отображения зон групп
			for i in mesh:
				i['faces'] = getFacesFromVert(i['vertices'])
			# записываем зоны входа
			for j in mesh:
				for i in args['izoneuzone']:
					if i.UserZone_id == j['id']:
						j['izones'].append({'id': i.IncomeZone_id, \
						 'vertices': [], 'faces': []})
			 	for iz in j['izones']:
			 		for v in args['vzones']:
			 			if iz['id'] == v.IncomeZone_id:
			 				iz['vertices'].append({'x': v.xCoord, 'y': v.yCoord, \
			 				 'zmin': v.zmin, 'zmax': v.zmax})
	 				iz['faces'] = getFacesFromVert(iz['vertices'])
			# записываем зоны исключения
			for j in mesh:
				for i in args['ezoneuzone']:
					if i.UserZone_id == j['id']:
						j['ezones'].append({'id': i.ExcludeZone_id, \
							'vertices': [], 'faces': []})
				for ez in j['ezones']:
					for v in args['evzones']:
						if ez['id'] == v.ExcludeZone_id:
							ez['vertices'].append({'x': v.xCoord, 'y': v.yCoord, \
								'zmin': v.zmin, 'zmax': v.zmax})
					ez['faces'] = getFacesFromVert(ez['vertices'])
			args['data'] = {}
			args['data']['mesh'] = mesh
			args['data']['userzonetable'] = render_to_string('userzonetable.html', args)
			return JsonResponse(args['data'])
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
		# показываем запрашиваемую зону userzone
		if string['method'] == 'show_uzone':
			obj = {}
			obj['uzone'] = []
			zoneid = string['zoneid']
			vertices = VerticesUserZone.objects.filter(UserZone_id=zoneid)
			vToSend = []
			for v in vertices:
				vToSend.append({'x': v.xCoord, 'y': v.yCoord, 'zmin': v.zmin, 'zmax': v.zmax})
			obj['uzone'].append({'id': zoneid, 'vertices': vToSend, \
				'faces': getFacesFromVert(vToSend), 'izones': [], 'ezones': []})
			# наполняем словарь incomezones
			for i in args['izoneuzone']:
				if i.UserZone_id == zoneid:
					obj['uzone'][0]['izones'].append({'id': i.IncomeZone_id, \
					 'vertices': [], 'faces': []})
		 	for iz in obj['uzone'][0]['izones']:
		 		for v in args['vzones']:
		 			if iz['id'] == v.IncomeZone_id:
		 				iz['vertices'].append({'x': v.xCoord, 'y': v.yCoord, \
		 				 'zmin': v.zmin, 'zmax': v.zmax})
 				iz['faces'] = getFacesFromVert(iz['vertices'])
			# наполняем словарь excludezones
			for i in args['ezoneuzone']:
				if i.UserZone_id == zoneid:
					obj['uzone'][0]['ezones'].append({'id': i.ExcludeZone_id, \
						'vertices': [], 'faces': []})
			for ez in obj['uzone'][0]['ezones']:
				for v in args['evzones']:
					if ez['id'] == v.ExcludeZone_id:
						ez['vertices'].append({'x': v.xCoord, 'y': v.yCoord, \
							'zmin': v.zmin, 'zmax': v.zmax})
				ez['faces'] = getFacesFromVert(ez['vertices'])
			return JsonResponse(obj)
		# создаем новую uzonegroup
		if string['method'] == 'adduzonegroup':
			username = string['user']
			GroupUserZone.objects.create(User_id=username, LoadLandscape_id=string['landscape_id'])
			args['uzonegroups'] = GroupUserZone.objects.filter(User_id=username, \
			 LoadLandscape_id=string['landscape_id'])
			return render(request, 'userzonegrouptable.html', args)
		#удаляем uzonegroup
		if string['method'] == 'deleteuzonegroup':
			username = string['user']
			uid = string['uid']
			GroupUserZone.objects.filter(id=uid, LoadLandscape_id=string['landscape_id']).delete()
			return render(request, 'userzonegrouptable.html', args)
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
				# ищем зоны пользователя для building
				zones = BuildingUserZone.objects.filter(Building_id=b.id)
				obj['uzone'] = []
				for z in zones:
					zoneid = z.UserZone_id
					# вершины
					vertices = VerticesUserZone.objects.filter(UserZone_id=zoneid)
					vToSend = []
					for v in vertices:
						vToSend.append({'x': v.xCoord, 'y': v.yCoord, 'zmin': v.zmin, 'zmax': v.zmax})
					obj['uzone'].append({'id': z.UserZone_id, 'vertices': vToSend, \
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
				# ищем зоны пользователя для floor
				zones = FloorUserZone.objects.filter(Floor_id=f.id)
				obj['uzone'] = []
				for z in zones:
					zoneid = z.UserZone_id
					# вершины
					vertices = VerticesUserZone.objects.filter(UserZone_id=zoneid)
					vToSend = []
					for v in vertices:
						vToSend.append({'x': v.xCoord, 'y': v.yCoord, 'zmin': v.zmin, 'zmax': v.zmax})
					obj['uzone'].append({'id': z.UserZone_id, 'vertices': vToSend, \
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
				# ищем зоны пользователя для kabinet
				zones = KabinetUserZone.objects.filter(Kabinet_id=k.id)
				obj['uzone'] = []
				for z in zones:
					zoneid = z.UserZone_id
					# вершины
					vertices = VerticesUserZone.objects.filter(UserZone_id=zoneid)
					vToSend = []
					for v in vertices:
						vToSend.append({'x': v.xCoord, 'y': v.yCoord, 'zmin': v.zmin, 'zmax': v.zmax})
					obj['uzone'].append({'id': z.UserZone_id, 'vertices': vToSend, \
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
	elif text == 'uzones':
		LoadLandscapeUserZone.objects.filter(UserZone_id=zoneid).delete()
		BuildingUserZone.objects.filter(UserZone_id=zoneid).delete()
		FloorUserZone.objects.filter(UserZone_id=zoneid).delete()
		KabinetUserZone.objects.filter(UserZone_id=zoneid).delete()

# принадлежность метки
def getbelong(request):
	string = simplejson.loads(request.body)
	user_id = string['user_id']
	tag_id = string['tag_id']
	if string['type'] == 'start':
		for a in active_users:
			if a['id'] == user_id:
				a['belong'] = {'tag_id': tag_id}
				return JsonResponse(string)
	if string['type'] == 'stop':
		for a in active_users:
			if a['id'] == user_id:
				if 'belong' in a:
					del a['belong']
				return JsonResponse(string)

# принадлежность метки зоне пользователя
def getbelonguzone(request):
	string = simplejson.loads(request.body)
	user_id = string['user_id']
	tag_id = string['tag_id']
	if string['type'] == 'start':
		for a in active_users:
			if a['id'] == user_id:
				a['belonguzone'] = {'tag_id': tag_id}
				return JsonResponse(string)
	if string['type'] == 'stop':
		for a in active_users:
			if a['id'] == user_id:
				if 'belonguzone' in a:
					del a['belonguzone']
				return JsonResponse(string)
# получить список объектов от сервера
def getobjectlistfromserver(request):
	args = {}
	args['username'] = auth.get_user(request).id
	args['objecttype'] = ObjectType.objects.all()
	if request.method == 'POST':
		string = simplejson.loads(request.body)
		# отправть запрос получить списки расхождений объектов типа между ВС и СП
		if string['method'] == 'difference':
			obj_type = string['obj_type']
			a = ObjectType.objects.get(id=obj_type)
			commandList = a.CommandList
			url = 'http://192.168.1.111:8000'
			data = json({"command": commandList})
			headers = {'content-type:': 'application/json', 'charset': 'utf-8'}
			args['ws'] = list(Object.objects.filter(objectobjecttype__ObjectType_id=obj_type).values( \
				'server_id', 'Name', 'Description', 'xCoord', 'yCoord', 'zCoord', 'server_inUse', \
				 'LoadLandscape__server_id', 'server_type', 'server_radius', 'server_minNumPoints'))
			try:
				r = requests.post(url, data=data, headers=headers)
				json_data = simplejson.loads(r.text)
				args['sp'] = list(json_data[a.Name_eng])
			except:
				args['error'] = 'сервер не отвечает'
				
			# меняем систему координат sp
			# for s in args['sp']:
			# 	s['x'] = s['z']
			# 	s['y'] = s['x']
			# 	s['z'] = s['y']

			# есть ws, нет sp
			for w in args['ws']:
				for s in args['sp']:
					if w['server_id'] == s['id']:
						w['got'] = 1
			haveinweb = []
			for w in args['ws']:
				if not('got' in w):
					haveinweb.append(w)
			args['haveinweb'] = haveinweb
			# есть sp, нет ws
			for s in args['sp']:
				for w in args['ws']:
					if s['id'] == w['server_id']:
						s['got'] = 1
			haveinsp = []
			for s in args['sp']:
				if not('got' in s):
					haveinsp.append(s)
			args['haveinsp'] = haveinsp
			args['getlisttable'] = render_to_string('getlistdifference.html', args)
			return JsonResponse({'string': args['getlisttable']})
		# отправить запрос получить список всех объектов типа от СП
		if string['method'] == 'sendrequest':
			obj_type = string['obj_type']
			a = ObjectType.objects.get(id=obj_type)
			commandList = a.CommandList
			url = 'http://192.168.1.111:8000'
			data = json({"command": commandList})
			headers = {'content-type:': 'application/json', 'charset': 'utf-8'}
			try:
				r = requests.post(url, data=data, headers=headers)
				json_data = simplejson.loads(r.text)
				args['json_data'] = list(json_data[a.Name_eng])
			except:
				args['error'] = 'сервер не отвечает'
			args['getlisttable'] = render_to_string('getlisttable.html', args)
			return JsonResponse({'string': args['getlisttable'], 'arr': args['json_data']})
		# отправить список объектов конкретного типа на ВС
		if string['method'] == 'loadtoserver':
			obj_type = string['obj_type']
			obj_server = string['objects']
			landscapes = list(LoadLandscape.objects.all())
			objects = list(Object.objects.all())
			for obj in obj_server:
				doubled = 0
				#eсли уже был записан, обновляем информацию
				for o in objects:
					if obj['id'] == o.server_id:
						o.Name = obj['name']
						o.Description = obj['description']
						o.xCoord = obj['x']
						o.yCoord = obj['z']
						o.zCoord = obj['y']
						o.server_inUse = obj['inUse']
						o.LoadLandscape_id = l['landscape_id']
						o.server_type = obj['type']
						o.server_radius = obj['radius']
						o.server_minNumPoints = obj['minNumPoints']
						o.save()
						doubled = 1
						break
				#новая запись
				if doubled == 0:
					for l in landscapes:
						if 'type' in obj:
							if obj['idLayer'] == l.server_id:
								a = Object.objects.create(Name=obj['name'], Description=obj['description'], \
									xCoord=obj['z'], yCoord=obj['x'], zCoord=obj['y'], \
									 server_inUse=obj['inUse'], LoadLandscape_id=l.landscape_id, \
									 server_type=obj['type'], server_radius=obj['radius'], \
									 server_minNumPoints=obj['minNumPoints'], server_id=obj['id'])
								ObjectObjectType.objects.create(Object_id=a.id, ObjectType_id=obj_type)
								break
						else:
							if obj['idLayer'] == l.server_id:
								a = Object.objects.create(Name=obj['name'], Description=obj['description'], \
									xCoord=obj['z'], yCoord=obj['x'], zCoord=obj['y'], \
									 server_inUse=obj['inUse'], LoadLandscape_id=l.landscape_id, \
									 server_type=False, server_radius=False, \
									 server_minNumPoints=False, server_id=obj['id'])
								ObjectObjectType.objects.create(Object_id=a.id, ObjectType_id=obj_type)
								break
			return JsonResponse({'string': 'ok'})
	return render(request, 'getobjectlistfromserver.html', args)