#!/usr/bin/python
# -*- coding: utf8 -*-
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from mainapp.models import *
from report.models import *
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import auth
from django.core import serializers
from operator import itemgetter
import datetime
import json
import requests
import redis
from django.conf import settings
try:
	from django.utils import simplejson
except:
	import simplejson
# выбор отчета
def reportselect(request):
	args = {}
	args['Report'] = Report.objects.all().values('id', 'Name', 'Description', 'reportuser__User_id')
	args['user'] = auth.get_user(request).id
	return render(request, 'reportselect.html', args)

# параметр отчета
def reportparameters(request, report=1):
	args = {}
	args['user'] = auth.get_user(request)
	args['report'] = Report.objects.get(id=report)
	args['tags'] = Tag.objects.all()
	# подбор параметров к отчету, заполнение html блоков отчета с параметрами
	args['reportparameters'] = ReportParameter.objects.filter(Report_id=args['report'].id).values( \
		'Parameter__domName', 'Parameter_id')
	for rp in args['reportparameters']:
		rp['html'] = render_to_string('%s.html' %(rp['Parameter__domName']), args)
	if request.method == 'POST':
		string = simplejson.loads(request.body)
		# Идентификатор / наименование
		# изменение значение inputselect name или tag_id
		if string['method'] == 'tagchange':
			args['name'] = Tag.objects.get(TagId=string['tag_id']).Name
			args['tag_id'] = string['tag_id']
			args['identselect'] = render_to_string('identselect.html', args)
			return JsonResponse({'string': args['identselect']})
		if string['method'] == 'namechange':
			args['name'] = Tag.objects.get(TagId=string['tag_id']).Name
			args['tag_id'] = Tag.objects.get(TagId=string['tag_id']).TagId
			args['identselect'] = render_to_string('identselect.html', args)
			return JsonResponse({'string': args['identselect']})
		# структурное подразделение / зона пользователя
		# структурное подразделение radio button
		if string['method'] == 'structure':
			args['radio'] = 'inuzone'
			# заполняем идентификатор сцены
			args['loadlandscapes'] = LoadLandscape.objects.all()
			return JsonResponse(structure(args))
		#изменен scene_id
		if string['method'] == 'scene_idchange':
			args['loadlandscapes'] = LoadLandscape.objects.all()
			args['landscape_id'] = string['landscape_id']
			return JsonResponse(structure(args))
		#изменен scenename
		if string['method'] == 'scenenamechange':
			args['loadlandscapes'] = LoadLandscape.objects.all()
			args['landscape_id'] = string['landscape_id']
			return JsonResponse(structure(args))
		#поставлен checkbox building
		if string['method'] == 'choosebuilding':
			args['landscape_id'] = string['landscape_id']
			args['buildings'] = Building.objects.filter(LoadLandscape_id=args['landscape_id'])
			args['buildingselect'] = render_to_string('buildingselect.html', args)
			return JsonResponse({'string': args['buildingselect']})
		#поставлен checkbox floor
		if string['method'] == 'choosefloor':
			args['building'] = string['building_id']
			args['floors'] = Floor.objects.filter(Building_id=args['building'])
			args['floorselect'] = render_to_string('floorselect.html', args)
			return JsonResponse({'string': args['floorselect']})
		#поставлен checkbox kabinet
		if string['method'] == 'choosekabinet':
			args['floor'] = string['floor_id']
			args['kabinets'] = Kabinet_n_Outer.objects.filter(Floor_id=args['floor']).exclude( \
				dae_Kabinet_n_OuterName__icontains='outer')
			args['kabinetselect'] = render_to_string('kabinetselect.html', args)
			return JsonResponse({'string': args['kabinetselect']})
		if string['method'] == 'inuzone':
			args['radio'] = 'inuzone'
			args['uzone'] = render_to_string('uzone.html', args)
			args['instructure'] = render_to_string('instructure.html', args)
			return JsonResponse({'string': args['instructure']})
		if string['method'] == 'uzoneselect':
			args['user_id'] = string['user_id']
			args['uzones'] = UserZone.objects.filter(User_id=args['user_id'])
			args['uzone'] = render_to_string('uzonelist.html', args)
			return JsonResponse({'string': args['uzone']})
		if string['method'] == 'uzonegroupselect':
			args['user_id'] = string['user_id']
			args['gruzones'] = GroupUserZone.objects.filter(User_id=args['user_id'])
			args['uzonegrouplist'] = render_to_string('uzonegrouplist.html', args) 
			return JsonResponse({'string': args['uzonegrouplist']})
		#отобразить ошибки на форме
		if string['method'] == 'showerrors':
			args['errors'] = string['errors']
			args['showerrors'] = render_to_string('showerrors.html', args)
			return JsonResponse({'string': args['showerrors']})
		##############################
		###сформировать отчет
		if string['method'] == 'getreport':
			# узнаем может ли в отчете объединения множества меток
			report_id = string['report_id']
			canbemultiple = Report.objects.get(id=report_id).CanBeMultipleTagId
			if canbemultiple == False:
				params = string['parameters']
				for p in params:
					if p['id'] == 1:
						# идентификатор
						identificator = p['parameters']
					if p['id'] == 2:
						# интервал
						interval = p['parameters']
					if p['id'] == 3:
						# подразделение
						str_n_uzone = p['parameters']
				# tag_id
				tag_id = identificator['tag_id']
				# interval
				strFrom = datetime.datetime.strptime(interval['from'], '%d-%m-%Y %H:%M')
				strTo = datetime.datetime.strptime(interval['to'], '%d-%m-%Y %H:%M')
				# structure
				# проверка есть ли building, floor, kabinet
				if 'structure' in str_n_uzone:
					#only landscape_id
					if ('kabinet_id' not in str_n_uzone) and ('floor_id' not in str_n_uzone) and \
					  ('building_id' not in str_n_uzone):
						turnonofftag = TurnOnOffTag.objects.filter(OnOffTime__gte=strFrom, OnOffTime__lte=strTo, \
						 Tag_id=tag_id)
						tagfloororder = TagFloorOrder.objects.filter(WriteTime__gte=strFrom, \
						 WriteTime__lte=strTo, Tag_id=tag_id)
						tagkabinetorder = TagKabinetOrder.objects.filter(WriteTime__gte=strFrom, \
							 WriteTime__lte=strTo, Tag_id=tag_id)
						tagoutofbuilding = TagOutOfBuilding.objects.filter(WriteTime__gte=strFrom, \
							 WriteTime__lte=strTo, Tag_id=tag_id)
						floors = Floor.objects.all()
						buildings = Building.objects.all()
						kabinets = Kabinet_n_Outer.objects.all()
						#создаем словарь перемещений
						chronology = []
						for toot in turnonofftag:
							#если включается-выключается метка
							parameters = {'on': toot.OnOff}
							chronology.append({'time': toot.OnOffTime, 'table': 'turnonofftag', \
							 'parameters': toot.OnOff})

						for tfo in tagfloororder:
							#если этаж
							parameters = {'floor_id': tfo.Floor_id}
							#ищем наименование этажей, зданий
							a = getObjName(parameters['floor_id'], 'floor', floors, buildings, kabinets)
							chronology.append({'time': tfo.WriteTime, 'table': 'tagfloororder', 'parameters': parameters, \
								'floorname': a['floorname'], 'buildingname': a['buildingname']})
						for tko in tagkabinetorder:
							#если кабинет
							parameters = {'kabinet_id': tko.Kabinet_n_Outer_id}
							#ищем наименование кабинетов, этажей, зданий
							a = getObjName(parameters['kabinet_id'], 'kabinet', floors, buildings, kabinets)
							chronology.append({'time':tko.WriteTime, 'table': 'tagkabinetorder', 'parameters':parameters, \
								 'kabinetname': a['kabinetname'], 'floorname': a['floorname'], \
								  'buildingname': a['buildingname']})


						for toob in tagoutofbuilding:
							#если выход из здания
							parameters = {}
							chronology.append({'time': toob.WriteTime, 'table': 'tagoutofbuilding', \
							 'parameters': parameters})

						args['chronology'] = sorted(chronology, key=lambda k: k['time'])
						# добавляем длительность пребывания
						no = 0
						for c in args['chronology']:
							if no < len(args['chronology'])-1:
								c['length'] = args['chronology'][no+1]['time'] - c['time']
								no += 1
						args['structure'] = render_to_string('structuretable.html', args)
						return JsonResponse({'string': args['structure']})
					#landscape_id, building_id
			  	elif ('kabinet_id' not in str_n_uzone) and ('floor_id' not in str_n_uzone):
			  		pass
		  		#landscape_id, building_id, floor_id
		  		elif ('kabinet_id' not in str_n_uzone):
		  			pass
	return render(request, 'reportparameters.html', args)

def getKabinet(Kabinet, ObjId):
	returnedDict = {}
	for k in Kabinet:
		if k.id == ObjId:
			returnedDict['floor_id'] = k.Floor_id
			if k.Kabinet_n_OuterName:
				returnedDict['kabinetname'] = k.Kabinet_n_OuterName
			else:
				returnedDict['kabinetname'] = k.dae_Kabinet_n_OuterName
			break
	return returnedDict

def getFloor(Floor, ObjId):
	returnedDict = {}
	for f in Floor:
		if f.id == ObjId:
			returnedDict['building_id'] = f.Building_id
			if f.FloorName:
				returnedDict['floorname'] = f.FloorName
			else:
				returnedDict['floorname'] = f.dae_FloorName
			break
	return returnedDict	

def getBuilding(Building, ObjId):
	returnedDict = {}
	for b in Building:
		if b.id == ObjId:
			if b.BuildingName:
				returnedDict['buildingname'] = b.BuildingName
			else:
				returnedDict['buildingname'] = b.dae_BuildingName
			break
	return returnedDict

def getObjName(ObjId, ObjType, Floor, Building, Kabinet):
	returnedDict = {}
	if ObjType == 'floor':
		a = getFloor(Floor, ObjId)
		returnedDict['floorname'] = a['floorname']
		a = getBuilding(Building, a['building_id'])
		returnedDict['buildingname'] = a['buildingname']
		return returnedDict
	if ObjType == 'kabinet':
		a = getKabinet(Kabinet, ObjId)
		returnedDict['kabinetname'] = a['kabinetname']
		a = getFloor(Floor, a['floor_id'])
		returnedDict['floorname'] = a['floorname']
		a = getBuilding(Building, a['building_id'])
		returnedDict['buildingname'] = a['buildingname']
		return returnedDict

def structure(arr):
	arr['radio'] = 'instructure'
	arr['structure'] = render_to_string('structure.html', arr)
	arr['instructure'] = render_to_string('instructure.html', arr)
	return {'string': arr['instructure']}