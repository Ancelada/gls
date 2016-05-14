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
	report_uzone = ReportUzone.objects.get(Report_id=int(report))
	report_structure = ReportStructure.objects.get(Report_id=int(report))
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
			args['landscapeselect'] = render_to_string('landscapeselect.html', args)
			return JsonResponse(structure(args))
		#изменен scenename
		if string['method'] == 'scenenamechange':
			args['loadlandscapes'] = LoadLandscape.objects.all()
			args['landscape_id'] = string['landscape_id']
			args['landscapeselect'] = render_to_string('landscapeselect.html', args)
			return JsonResponse(structure(args))
		#поставлен checkbox landscape
		if string['method'] == 'chooselandscape':
			args['loadlandscapes'] = LoadLandscape.objects.all()
			args['landscapeselect'] = render_to_string('landscapeselect.html', args)
			return JsonResponse({'string': args['landscapeselect']})
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
				args['strFrom'] = strFrom
				args['strTo'] = strTo
				# structure
				################
				# проверка есть ли building, floor, kabinet
				if not 'structure' in str_n_uzone and not 'uzone' in str_n_uzone:
					# (get all) no landscape, no building, no floors etc
					#############################
					args['chronology'] = getAll(strFrom, strTo, tag_id)
					args['structurelength'] = groupStructureByLength(args['chronology'])
					args[report_structure.TemplateParameter] = \
					 render_to_string(report_structure.TemplateFileName, args)
					return JsonResponse({'string': args[report_structure.TemplateParameter]})
				if 'structure' in str_n_uzone:
					chronology = getAll(strFrom, strTo, tag_id)
					#only landscape_id
					#######################
					if ('kabinet_id' not in str_n_uzone['structure']) \
					 and ('floor_id' not in str_n_uzone['structure']) \
					  and  ('building_id' not in str_n_uzone['structure']) \
					   and ('landscape_id' in str_n_uzone['structure']):
						args['chronology'] = getByType('landscape_id', chronology, str_n_uzone)
						args['structurelength'] = groupStructureByLength(args['chronology'])
						args[report_structure.TemplateParameter] = \
					 render_to_string(report_structure.TemplateFileName, args)
						return JsonResponse({'string': args[report_structure.TemplateParameter]})
					#landscape_id, building_id
					###############################
					elif ('kabinet_id' not in str_n_uzone['structure']) \
					 and('floor_id' not in str_n_uzone['structure']) \
					  and('building_id' in str_n_uzone['structure']):
					  	args['chronology'] = getByType('building_id', chronology, str_n_uzone)
					  	args['structurelength'] = groupStructureByLength(args['chronology'])
				  		args[report_structure.TemplateParameter] = \
					 render_to_string(report_structure.TemplateFileName, args)
					  	return JsonResponse({'string': args[report_structure.TemplateParameter]})
					#landscape_id, building_id, floor_id
					###############################
					if ('kabinet_id' not in str_n_uzone['structure']) \
					 and ('floor_id' in str_n_uzone['structure']):
						args['chronology'] = getByType('floor_id', chronology, str_n_uzone)
						args['structurelength'] = groupStructureByLength(args['chronology'])
						args[report_structure.TemplateParameter] = \
					 render_to_string(report_structure.TemplateFileName, args)
						return JsonResponse({'string': args[report_structure.TemplateParameter]})
					#landscape_id, building_id, floor_id, kabinet_id
					###############################
					if ('kabinet_id' in str_n_uzone['structure']):
						args['chronology'] = getByType('kabinet_id', chronology, str_n_uzone)
						args['structurelength'] = groupStructureByLength(args['chronology'])
						args[report_structure.TemplateParameter] = \
					 render_to_string(report_structure.TemplateFileName, args)
						return JsonResponse({'string': args[report_structure.TemplateParameter]})
				# userzone
				################
				if 'uzone' in str_n_uzone:
					# если не указана конкретная зона пользователя, отобразить перемещения по всем зонам
					chronology = getAllUz(strFrom, strTo, tag_id, args['user'])
					if 'userzone' in str_n_uzone['uzone']:
						if str_n_uzone['uzone']['userzone'] == 'all':
							args['chronology'] = chronology
							args['uzonelength'] = groupUzoneByLength(args['chronology'])
							args[report_uzone.TemplateParameter] = \
							 render_to_string(report_uzone.TemplateFileName, args)
						elif str_n_uzone['uzone']['userzone'] != 'all':
							# указана зона пользователя
							args['chronology'] = getUzoneByType('userzone', chronology, str_n_uzone)
							args['uzonelength'] = groupUzoneByLength(args['chronology'])
							args[report_uzone.TemplateParameter] = \
							 render_to_string(report_uzone.TemplateFileName, args)
					# если не указана конкретная зона пользователя, отобразить перемещения по всем зонам
					elif 'groupuzone' in str_n_uzone['uzone']:
						if str_n_uzone['uzone']['groupuzone'] == 'all':
							args['chronology'] = chronology
							args['uzonelength'] = groupUzoneByLength(args['chronology'])
							args[report_uzone.TemplateParameter] = \
							 render_to_string(report_uzone.TemplateFileName, args)
						elif str_n_uzone['uzone']['groupuzone'] != 'all':
							# указана группа зон пользователя
							args['chronology'] = getUzoneByType('groupuzone', chronology, str_n_uzone)
							args['uzonelength'] = groupUzoneByLength(args['chronology'])
							args[report_uzone.TemplateParameter] = \
							 render_to_string(report_uzone.TemplateFileName, args)
					return JsonResponse({'string': args[report_uzone.TemplateParameter]})
	return render(request, 'reportparameters.html', args)

def groupUzoneByLength(chronology):
	newArr = []
	for i in chronology:
		doubled = 0
		if len(newArr) == 0:
			ifKeyUzoneInArrayFind(i, newArr)
		for j in newArr:
			if i['eventtype'] == j['eventtype']:
				if 'length' in i:
					j['length'] += i['length']
				doubled = 1
		if doubled == 0:
			if 'length' in i:
				ifKeyUzoneInArrayFind(i, newArr)
	return newArr

def ifKeyUzoneInArrayFind(i, newArr):
	if 'uzonename' in i:
		newArr.append({'eventtype': i['eventtype'], 'landscapename': i['landscapename'], \
			 'uzonename': i['uzonename'], 'gruzonename': i['gruzonename'], 'length': i['length'], \
			  'color': i['color']})
	else:
		if 'length' in i:
			newArr.append({'eventtype': i['eventtype'], 'length': i['length'], 'color': i['color']})

def groupStructureByLength(chronology):
	newArr = []
	for i in chronology:
		doubled = 0
		if len(newArr) == 0:
			ifKeyStructureInArrayFind(i, newArr)
		for j in newArr:
			if i['eventtype'] == j['eventtype']:
				if 'length' in i:
					j['length'] += i['length']
				doubled = 1
		if doubled == 0:
			if 'length' in i:
				ifKeyStructureInArrayFind(i, newArr)
	return newArr

def ifKeyStructureInArrayFind(i, newArr):
	if 'landscapename' in i and 'buildingname' in i and 'floorname' in i and 'kabinetname' in i:
		newArr.append({'eventtype': i['eventtype'], 'length': i['length'], 'color': i['color'], \
			 'landscapename': i['landscapename'], 'buildingname': i['buildingname'], \
			  'floorname': i['floorname'], 'kabinetname': i['kabinetname']})
	elif 'landscapename' in i and 'buildingname' in i and 'floorname' in i \
	 and not 'kabinetname' in i:
		newArr.append({'eventtype': i['eventtype'], 'length': i['length'], 'color': i['color'], \
		 'landscapename': i['landscapename'], 'buildingname': i['buildingname'], \
		 'floorname': i['floorname']})
	else:
		if 'length' in i:
			newArr.append({'eventtype': i['eventtype'], 'length': i['length'], 'color': i['color']})

def getByType(Type, chronology, str_n_uzone):
	newArr = []
	for c in chronology:
		if (c['table'] == 'tagoutofbuilding' or c['table'] == 'turnonofftag') and \
		 c['parameters']['landscape_id'] == str_n_uzone['structure']['landscape_id']:
			newArr.append(c)
		elif Type in c['parameters']:
			if c['parameters'][Type] == str_n_uzone['structure'][Type]:
				newArr.append(c)
	return newArr

def getUzoneByType(Type, chronology, str_n_uzone):
	newArr = []
	for c in chronology:
		if (c['table'] == 'turnonofftag' or c['table'] == 'tagnouzone'):
			newArr.append(c)
		elif Type in c['parameters']:
			if c['parameters'][Type] == str_n_uzone['uzone'][Type]['id']:
				newArr.append(c)
	return newArr

def getAllUz(strFrom, strTo, tag_id, user):
	turnonofftag = TurnOnOffTag.objects.filter(OnOffTime__gte=strFrom, OnOffTime__lte=strTo, \
		 Tag_id=tag_id)
	tagnouzone = TagNoUzone.objects.filter(Tag_id=tag_id, User_id=user, WriteTime__gte=strFrom, \
	 WriteTime__lte=strTo)
	taguzoneuserorder = TagUzoneUserOrder.objects.filter(Tag_id=tag_id, WriteTime__gte=strFrom, \
	 WriteTime__lte=strTo, User_id=user).values('WriteTime', 'Tag_id', \
	  'User_id', 'UserZone_id', 'UserZone__LoadLandscape_id')
	groupuserzoneuserzone = GroupUserZoneUserZone.objects.all()
	#создаем словарь перемещений
	chronology = []
	for toot in turnonofftag:
		#если включается-выключается метка
		parameters = {'on': toot.OnOff, 'landscape_id': toot.LoadLandscape_id}
		chronology.append({'time': toot.OnOffTime, 'table': 'turnonofftag', \
		 'parameters': parameters, 'landscapename': toot.LoadLandscape_id})
	for tnuz in tagnouzone:
		#если отсутствует uzone
		parameters = {'landscape_id': tnuz.LoadLandscape_id}
		chronology.append({'time': tnuz.WriteTime, 'table': 'tagnouzone', \
			 'parameters': parameters, 'landscapename': tnuz.LoadLandscape_id})
	for tuuo in taguzoneuserorder:
		#перемещения в зоны
		for i in groupuserzoneuserzone:
			if i.UserZone_id == tuuo['UserZone_id']:
				gruzone_id = i.GroupUserZone_id
		if gruzone_id:
			parameters = {'landscape_id': tuuo['UserZone__LoadLandscape_id'], \
			 'groupuzone': gruzone_id, 'userzone': tuuo['UserZone_id']}
			uzonename = uzoneName(tuuo['UserZone_id'], 'uzone')
			gruzonename = uzoneName(gruzone_id, 'gruzone')
		  	chronology.append({'time': tuuo['WriteTime'], 'gruzonename': gruzonename['groupuserzonename'], \
		  	 'uzonename': uzonename['userzonename'], \
		  	 'table': 'taguzoneuserorder', 'parameters': parameters, \
		  	  'landscapename': tuuo['UserZone__LoadLandscape_id']})
		else:
			parameters = {'landscape_id': tuuo['UserZone__LoadLandscape_id'], \
			 'userzone': tuuo['UserZone_id']}
			uzonename = uzoneName(tuuo['UserZone_id'], 'uzone')
		  	chronology.append({'time': tuuo['WriteTime'], 'table': 'taguzoneuserorder', \
		  		 'uzonename': uzonename['userzonename'], 'parameters': parameters, \
		  		  'landscapename': tuuo['UserZone__LoadLandscape_id']})
	chronology = sorted(chronology, key=lambda k: k['time'])
	# добавляем время до следующего события
	no = 0
	for c in chronology:
		if no < len(chronology)-1:
			c['length'] = chronology[no+1]['time'] - c['time']
			no += 1
	# добавляем поля eventtype, color тип события, цвет
	for c in chronology:
		if c['table'] == 'taguzoneuserorder':
			c['eventtype'] = u'Переход в зону %s' %(c['uzonename'])
			c['color'] = 'c9c9ff'
		elif c['table'] == 'turnonofftag' and c['parameters']['on'] == True:
			c['eventtype'] = u'Включение метки'
			c['color'] = 'e8ffb2'
		elif c['table'] == 'turnonofftag' and c['parameters']['on'] == False:
			c['eventtype'] = u'Выключение метки'
			c['color'] = 'ffbdbd'
		elif c['table'] == 'tagnouzone':
			c['eventtype'] = u'Выход из зон'
			c['color'] = 'eecbff'
	return chronology

def getAll(strFrom, strTo, tag_id):
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
	landscapes = LoadLandscape.objects.all()
	#создаем словарь перемещений
	chronology = []
	for toot in turnonofftag:
		#если включается-выключается метка
		parameters = {'on': toot.OnOff, 'landscape_id': toot.LoadLandscape_id}
		chronology.append({'time': toot.OnOffTime, 'table': 'turnonofftag', \
		 'parameters': parameters})

	for tfo in tagfloororder:
		#если этаж
		parameters = {}
		parameters['floor_id'] = tfo.Floor_id
		#ищем наименование этажей, зданий
		a = getObjName(parameters['floor_id'], 'floor', floors, buildings, kabinets, landscapes)
		parameters['landscape_id'] = a['landscape_id']
		parameters['building_id'] = a['building_id']
		chronology.append({'time': tfo.WriteTime, 'table': 'tagfloororder', 'parameters': parameters, \
			'floorname': a['floorname'], 'buildingname': a['buildingname'], \
			 'landscapename': a['landscapename']})
	for tko in tagkabinetorder:
		#если кабинет
		parameters = {}
		parameters['kabinet_id'] = tko.Kabinet_n_Outer_id
		#ищем наименование кабинетов, этажей, зданий
		a = getObjName(parameters['kabinet_id'], 'kabinet', floors, buildings, kabinets, landscapes)
		parameters['landscape_id'] = a['landscape_id']
		parameters['floor_id'] = a['floor_id']
		parameters['building_id'] = a['building_id']
		chronology.append({'time':tko.WriteTime, 'table': 'tagkabinetorder', 'parameters':parameters, \
			 'kabinetname': a['kabinetname'], 'floorname': a['floorname'], \
			  'buildingname': a['buildingname'], 'landscapename': a['landscapename']})


	for toob in tagoutofbuilding:
		#если выход из здания
		parameters = {'landscape_id': toob.LoadLandscape_id}
		chronology.append({'time': toob.WriteTime, 'table': 'tagoutofbuilding', \
		 'parameters': parameters})

	chronology = sorted(chronology, key=lambda k: k['time'])
	# добавляем время до следующего события
	no = 0
	for c in chronology:
		if no < len(chronology)-1:
			c['length'] = chronology[no+1]['time'] - c['time']
			no += 1
	# добавляем поля eventtype, color тип события, цвет
	for c in chronology:
		if c['table'] == 'tagkabinetorder':
			c['eventtype'] = u'Переход в кабинет %s' %(c['kabinetname'])
			c['color'] = 'c9c9ff'
		elif c['table'] == 'tagfloororder':
			c['eventtype'] = u'Перемещение на этаж %s' %(c['floorname'])
			c['color'] = 'feffa3'
		elif c['table'] == 'turnonofftag' and c['parameters']['on'] == True:
			c['eventtype'] = u'Включение метки'
			c['color'] = 'e8ffb2'
		elif c['table'] == 'turnonofftag' and c['parameters']['on'] == False:
			c['eventtype'] = u'Выключение метки'
			c['color'] = 'ffbdbd'
		elif c['table'] == 'tagoutofbuilding':
			c['eventtype'] = u'Выход из здания'
			c['color'] = 'eecbff'
	return chronology

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
			returnedDict['floor_id'] = f.id
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
			returnedDict['building_id'] = b.id
			break
	return returnedDict

def getLandscape(Landscape, Building, building_id):
	returnedDict = {}
	for b in Building:
		if b.id == building_id:
			landscape_id = b.LoadLandscape_id
			break
	for l in Landscape:
		if l.landscape_id == landscape_id:
			if l.landscape_name:
				returnedDict['landscapename'] = l.landscape_name
			else:
				returnedDict['landscapename'] = l.landscape_id
			returnedDict['landscape_id'] = l.landscape_id
			break
	return returnedDict

def getObjName(ObjId, ObjType, Floor, Building, Kabinet, Landscape):
	returnedDict = {}
	if ObjType == 'floor':
		a = getFloor(Floor, ObjId)
		returnedDict['floorname'] = a['floorname']
		returnedDict['floor_id'] = a['floor_id']
		building_id = a['building_id']
		a = getBuilding(Building, a['building_id'])
		returnedDict['buildingname'] = a['buildingname']
		returnedDict['building_id'] = a['building_id']
		a = getLandscape(Landscape, Building, building_id)
		returnedDict['landscapename'] = a['landscapename']
		returnedDict['landscape_id'] = a['landscape_id']
		return returnedDict
	if ObjType == 'kabinet':
		a = getKabinet(Kabinet, ObjId)
		returnedDict['kabinetname'] = a['kabinetname']
		a = getFloor(Floor, a['floor_id'])
		returnedDict['floorname'] = a['floorname']
		returnedDict['floor_id'] = a['floor_id']
		building_id = a['building_id']
		a = getBuilding(Building, a['building_id'])
		returnedDict['buildingname'] = a['buildingname']
		returnedDict['building_id'] = a['building_id']
		a = getLandscape(Landscape, Building, building_id)
		returnedDict['landscapename'] = a['landscapename']
		returnedDict['landscape_id'] = a['landscape_id']
		return returnedDict

def uzoneName(ObjId, ObjType):
	returnedDict = {}
	if ObjType == 'uzone':
		returnedDict['userzonename'] = UserZone.objects.get(id=ObjId).UserZoneName
	if ObjType == 'gruzone':
		returnedDict['groupuserzonename'] = GroupUserZone.objects.get(id=ObjId).GroupName
	return returnedDict

def structure(arr):
	arr['radio'] = 'instructure'
	arr['structure'] = render_to_string('structure.html', arr)
	arr['instructure'] = render_to_string('instructure.html', arr)
	return {'string': arr['instructure']}