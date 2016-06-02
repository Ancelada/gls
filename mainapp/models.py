#!/usr/bin/python
# -*- coding: utf8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import jsonfield
from time import time

# def get_upload_file_name(instance, filename):
# 	return 'uploaded_files/%s_%s' % (str(time).replace('.', '_'), filename)

# Create your models here.

class Metka(models.Model):
	class Meta():
		db_table = 'Metka'
	text = models.TextField()
	DateImport = models.DateTimeField(auto_now=True, null=True)
	readed = models.NullBooleanField(null=True)

#####################
# СООБЩЕНИЯ SLMP
#####################



# типы данных(из ТЗ Пиложение 4, быть может не нужно)
class DataType(models.Model):
	class Meta():
		db_table = 'DataType'
	DataTypeName = models.CharField(max_length=200)
	DjangoFormat = models.CharField(max_length=200)
	def __str__(self):
		return self.DataTypeName.encode('utf-8')
# конец типы данных


# сообщения с определениями полей(из ТЗ Пиложение 4, быть может не нужно)
class Field_Definition_Message(models.Model):
	class Meta():
		db_table = 'Field_Definition_Message'
	Field_Definition_MessageName = models.CharField(max_length=200)
	XmlTag = models.CharField(max_length=50)
	DataType = models.ForeignKey(DataType)
	LengthMin = models.IntegerField(null=False, default=0)
	LengthMax = models.IntegerField(null=False, default=0)
	def __str__(self):
		return self.Field_Definition_MessageName.encode('utf-8')
# конец сообщений с определениями полей

# тип формата определения сообщений местонахождения(из ТЗ Пиложение 4, быть может не нужно)
class LMDMFormat(models.Model):
	class Meta():
		db_table = 'LMDM_Format'
	LMDMFormatName = models.CharField(max_length=200)
	def __str__(self):
		return self.LMDMFormatName.encode('utf-8')
# конец типа формата определения сообщений местонахождения

# сообщения с oпределениями формата сообщений местонахождения(из ТЗ Пиложение 4, быть может не нужно)
class Locate_Message_Definition_Message(models.Model):
	class Meta():
		db_table = 'Locate_Message_Definition_Message'
	Source = models.CharField(max_length=200)
	Format = models.ForeignKey(LMDMFormat)
	def __str__(self):
		return self.Source.encode('utf-8')
# конец сообщения с определениями формата сообщений местонахождения


######################## запись сообщение в различных форматах: ############################
class Std0(models.Model):
	class Meta():
		db_table  = 'Std0'
	LocateMessageDefinition = models.CharField(max_length=200, null=True)
	LabD = models.CharField(max_length=200, null=True)
	Std0 = models.CharField(max_length=200, null=True)
	Tag_ID_Format = models.CharField(max_length=200, null=True)
	Tag_ID = models.CharField(max_length=200, null=True)
	X = models.FloatField(null=True)
	Y = models.FloatField(null=True)
	Z = models.FloatField(null=True)
	Battery = models.IntegerField(null=True)
	Timestamp = models.CharField(max_length=25, null=True)
	Status = models.CharField(max_length=1, null=True)
	Session = models.CharField(max_length=8, null=True)
	Zone = models.CharField(max_length=200, null=True)
	DateImport = models.DateTimeField(auto_now=True, null=True)
	TimeDelta = models.IntegerField(default=0, null=False)

######################## конец записи сообщений по форматам: ############################

###################
# КОНЕЦ СООБЩЕНИЯ SLMP
###################

###################
# ЖУРНАЛ ПЕРИОДИЧЕСКИХ ЗАДАНИЙ
###################
class LogsJournal(models.Model):
	class Meta():
		db_table = 'LogsJournal'
	CommandName = models.CharField(max_length=200)
	ResponseText = models.CharField(max_length=200)
	DateImport = models.DateTimeField(auto_now=True, null=True)
###################
# КОНЕЦ ЖУРНАЛА ПЕРИОДИЧЕСКИХ ЗАДАНИЙ
###################

###################
#РАБОТА СО СЦЕНАМИ
###################
class LoadLandscape(models.Model):
	class Meta():
		db_table = 'LoadLandscape'
	landscape_name = models.CharField(max_length=100)
	landscape_id = models.CharField(primary_key=True, max_length=20)
	landscape_source = models.FileField(upload_to='%s', blank=True, null=True)
	camera_position_x = models.FloatField(null=True)
	camera_position_y = models.FloatField(null=True)
	camera_position_z = models.FloatField(null=True)
	camera_up_x = models.FloatField(null=True)
	camera_up_y = models.FloatField(null=True)
	camera_up_z = models.FloatField(null=True)
	controls_target_x = models.FloatField(null=True)
	controls_target_y = models.FloatField(null=True)
	controls_target_z = models.FloatField(null=True)
	dae_rotation_x = models.FloatField(null=True)
	dae_rotation_y = models.FloatField(null=True)
	dae_rotation_z = models.FloatField(null=True)
	dae_position_x = models.FloatField(null=True)
	dae_position_y = models.FloatField(null=True)
	dae_position_z = models.FloatField(null=True)
	circle_step_symbol = models.BooleanField()
	get_wall_height_symbol = models.BooleanField()
	light_target_symbol = models.BooleanField()
	server_id = models.IntegerField(blank=True, null=True)
	session_id = models.IntegerField(blank=True, null=True)
	def __str__(self):
		return self.landscape_id.encode('utf-8')
class Building(models.Model):
	class Meta():
		db_table = 'Building'
	BuildingName = models.CharField(max_length=200, null=True)
	dae_BuildingName = models.CharField(max_length=200)
	minx = models.FloatField(null=True)
	miny = models.FloatField(null=True)
	minz = models.FloatField(null=True)
	maxx = models.FloatField(null=True)
	maxy = models.FloatField(null=True)
	maxz = models.FloatField(null=True)
	LoadLandscape = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE)

class VerticesBuilding(models.Model):
	class Meta():
		db_table = 'VerticesBuilding'
	x = models.FloatField(null=True)
	y = models.FloatField(null=True)
	Building = models.ForeignKey(Building, on_delete=models.CASCADE)
	LoadLandscape = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE)

class Floor(models.Model):
	class Meta():
		db_table = 'Floor'
	FloorName = models.CharField(max_length=200, null=True)
	dae_FloorName = models.CharField(max_length=200)
	minx = models.FloatField(null=True)
	miny = models.FloatField(null=True)
	minz = models.FloatField(null=True)
	maxx = models.FloatField(null=True)
	maxy = models.FloatField(null=True)
	maxz = models.FloatField(null=True)
	Building = models.ForeignKey(Building)
	LoadLandscape = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE)

class VerticesFloor(models.Model):
	class Meta():
		db_table = 'VerticesFloor'
	x = models.FloatField(null=True)
	y = models.FloatField(null=True)
	Floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
	LoadLandscape = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE)

class Kabinet_n_Outer(models.Model):
	class Meta():
		db_table = 'Kabinet_n_Outer'
	Kabinet_n_OuterName = models.CharField(max_length=200, null=True)
	dae_Kabinet_n_OuterName = models.CharField(max_length=200)
	minx = models.FloatField(null=True)
	miny = models.FloatField(null=True)
	minz = models.FloatField(null=True)
	maxx = models.FloatField(null=True)
	maxy = models.FloatField(null=True)
	maxz = models.FloatField(null=True)
	Floor = models.ForeignKey(Floor)
	LoadLandscape = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE)

class VerticesKabinet_n_Outer(models.Model):
	class Meta():
		db_table = 'VerticesKabinet_n_Outer'
	x = models.FloatField(null=True)
	y = models.FloatField(null=True)
	Kabinet_n_Outer = models.ForeignKey(Kabinet_n_Outer, on_delete=models.CASCADE)
	LoadLandscape = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE)

class Wall(models.Model):
	class Meta():
		db_table = 'Wall'
	WallName = models.CharField(max_length=200, null=True)
	dae_WallName = models.CharField(max_length=200)
	minx = models.FloatField(null=True)
	miny = models.FloatField(null=True)
	minz = models.FloatField(null=True)
	maxx = models.FloatField(null=True)
	maxy = models.FloatField(null=True)
	maxz = models.FloatField(null=True)
	Kabinet_n_Outer = models.ForeignKey(Kabinet_n_Outer, on_delete=models.CASCADE)
	LoadLandscape = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE)

######################
### Tags
######################


class TagGroup(models.Model):
	class Meta():
		db_table = 'TagGroup'
	GroupName = models.CharField(max_length=200, null=True, blank=True)
	MeshGeometry = jsonfield.JSONField(null=True, blank=True)
	MeshColor = models.CharField(max_length=50, null=True, blank=True)
	CircleColor = models.CharField(max_length=50, null=True, blank=True)
	User = models.ForeignKey(User, on_delete=models.CASCADE)
	def __str__(self):
		return self.GroupName.encode('utf-8')

class TagType(models.Model):
	class Meta():
		db_table = 'TagType'
	Name = models.CharField(max_length=200)
	def __str__(self):
		return self.Name.encode('utf-8')

class Tag(models.Model):
	class Meta():
		db_table = 'Tag'
	TagId = models.CharField(primary_key=True, max_length=20)
	Name = models.CharField(max_length=200, null=True)
	TagType = models.ForeignKey(TagType, on_delete=models.CASCADE)
	Registered = models.NullBooleanField(blank=True, null=True)
	def __str__(self):
		return self.TagId.encode('utf-8')

class TagGroup_Tag(models.Model):
	class Meta():
		db_table = 'TagGroup_Tag'
	TagGroup = models.ForeignKey(TagGroup)
	Tag = models.ForeignKey(Tag)
	User = models.ForeignKey(User, on_delete=models.CASCADE)

class LocationMethods(models.Model):
	class Meta():
		db_table = 'LocationMethods'
	ParameterName = models.CharField(max_length=200, blank=True, null=True)
	def __str__(self):
		return self.ParameterName.encode('utf-8')

class TagLocationMethods(models.Model):
	class Meta():
		db_table = 'TagLocationMethods'
	Tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	LocationMethods = models.ForeignKey(LocationMethods)

class Sensors(models.Model):
	class Meta():
		db_table = 'Sensors'
	ParameterName = models.CharField(max_length=200, blank=True, null=True)
	def __str__(self):
		return self.ParameterName.encode('utf-8')

class TagSensors(models.Model):
	class Meta():
		db_table = 'TagSensors'
	Tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	Sensors = models.ForeignKey(Sensors, on_delete=models.CASCADE)

class TimeUpdateLocation(models.Model):
	class Meta():
		db_table = 'TimeUpdateLocation'
	ParameterName = models.CharField(max_length=200, blank=True, null=True)
	def __str__(self):
		return self.ParameterName.encode('utf-8')

class TagTimeUpdateLocation(models.Model):
	class Meta():
		db_table = 'TagTimeUpdateLocation'
	Tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	TimeUpdateLocation = models.ForeignKey(TimeUpdateLocation, on_delete=models.CASCADE)
	Value = models.CharField(max_length=200, blank=True, null=True)

class CorrectionFilter(models.Model):
	class Meta():
		db_table = 'CorrectionFilter'
	ParameterName = models.CharField(max_length=200, blank=True, null=True)
	ParameterValueType = models.CharField(max_length=200, blank=True, null=True)
	def __str__(self):
		return self.ParameterName.encode('utf-8')

class TagCorrectionFilter(models.Model):
	class Meta():
		db_table = 'TagCorrectionFilter'
	Tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	CorrectionFilter = models.ForeignKey(CorrectionFilter, on_delete=models.CASCADE)
	Value = models.CharField(max_length=200, blank=True, null=True)

#############################
#### Nodes
##########################
class Node(models.Model):
	class Meta():
		db_table = 'Node'
	Name = models.CharField(max_length=200)
	Description = models.TextField()
	server_id = models.BigIntegerField(null=True, blank=True)
	def __str__(self):
		return self.Name.encode('utf-8')

class TagNode(models.Model):
	class Meta():
		db_table = 'TagNode'
	Tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True)
	Node = models.ForeignKey(Node, on_delete=models.CASCADE, null=True)

######################
### События
######################

class ZoneChange(models.Model):
	class Meta():
		db_table = 'ZoneChange'
	Tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	ZoneNew = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE)
	ChangeTime = models.DateTimeField(null=True)


class BldChange(models.Model):
	class Meta():
		db_table = 'BldChange'
	Tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	BldNew = models.ForeignKey(Building, on_delete=models.CASCADE)
	ChangeTime = models.DateTimeField(null=True)

class FlrChange(models.Model):
	class Meta():
		db_table = 'FlrChange'
	Tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	FlrNew = models.ForeignKey(Floor, on_delete=models.CASCADE)
	ChangeTime = models.DateTimeField(null=True)

class KbntChange(models.Model):
	class Meta():
		db_table = 'KbntChange'
	Tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	KbntNew = models.ForeignKey(Kabinet_n_Outer, on_delete=models.CASCADE)
	ChangeTime = models.DateTimeField(null=True)

class TurnOnOffTag(models.Model):
	class Meta():
		db_table = 'TurnOnOffTag'
	Tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	OnOff = models.BooleanField()
	OnOffTime = models.DateTimeField(null=True)
	LoadLandscape = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE)


###################
# Таблицы цветовой
# схемы сцен пользователей
###################
class LandscapeColor(models.Model):
	class Meta():
		db_table = 'LandscapeColor'
	User = models.ForeignKey(User, on_delete=models.CASCADE)
	lcolor = models.CharField(max_length=50, null=True, blank=True)
	LoadLandscape = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE)

class BuildingColor(models.Model):
	class Meta():
		db_table = 'BuildingColor'
	User = models.ForeignKey(User, on_delete=models.CASCADE)
	bcolor = models.CharField(max_length=50, null=True, blank=True)
	Building = models.ForeignKey(Building,  on_delete=models.CASCADE)

class FloorColor(models.Model):
	class Meta():
		db_table = "FloorColor"
	User = models.ForeignKey(User, on_delete=models.CASCADE)
	fcolor = models.CharField(max_length=50, null=True, blank=True)
	Floor = models.ForeignKey(Floor, on_delete=models.CASCADE)

class KabinetColor(models.Model):
	class Meta():
		db_table = "KabinetColor"
	User = models.ForeignKey(User, on_delete=models.CASCADE)
	kcolor = models.CharField(max_length=50, null=True, blank=True)
	Kabinet = models.ForeignKey(Kabinet_n_Outer, on_delete=models.CASCADE)

###################
# Зоны входа
###################
class IncomeZone(models.Model):
	class Meta():
		db_table = "IncomeZone"
	LoadLandscape = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE)

class VerticesIncomeZone(models.Model):
	class Meta():
		db_table = "VerticesIncomeZone"
	xCoord = models.FloatField()
	yCoord = models.FloatField()
	zmin = models.FloatField(blank=True, null=True)
	zmax = models.FloatField(blank=True, null=True)
	IncomeZone = models.ForeignKey(IncomeZone, on_delete=models.CASCADE)

class BuildingIncomeZone(models.Model):
	class Meta():
		db_table = "BuildingIncomeZone"
	Building = models.ForeignKey(Building, on_delete=models.CASCADE)
	IncomeZone = models.ForeignKey(IncomeZone, on_delete=models.CASCADE)

class FloorIncomeZone(models.Model):
	class Meta():
		db_table = 'FloorIncomeZone'
	Floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
	IncomeZone = models.ForeignKey(IncomeZone, on_delete=models.CASCADE)

class KabinetIncomeZone(models.Model):
	class Meta():
		db_table = 'KabinetIncomeZone'
	Kabinet = models.ForeignKey(Kabinet_n_Outer, on_delete=models.CASCADE)
	IncomeZone = models.ForeignKey(IncomeZone, on_delete=models.CASCADE)

####################
# Зоны исключения
####################
class ExcludeZone(models.Model):
	class Meta():
		db_table = "ExcludeZone"
	LoadLandscape = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE)

class VerticesExcludeZone(models.Model):
	class Meta():
		db_table = "VerticesExcludeZone"
	xCoord = models.FloatField()
	yCoord = models.FloatField()
	zmin = models.FloatField(blank=True, null=True)
	zmax = models.FloatField(blank=True, null=True)
	ExcludeZone = models.ForeignKey(ExcludeZone, on_delete=models.CASCADE)

class BuildingExcludeZone(models.Model):
	class Meta():
		db_table = "BuildingExcludeZone"
	Building = models.ForeignKey(Building, on_delete=models.CASCADE)
	ExcludeZone = models.ForeignKey(ExcludeZone, on_delete=models.CASCADE)

class FloorExcludeZone(models.Model):
	class Meta():
		db_table = "FloorExcludeZone"
	Floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
	ExcludeZone = models.ForeignKey(ExcludeZone, on_delete=models.CASCADE)

class KabinetExcludeZone(models.Model):
	class Meta():
		db_table = 'KabinetExcludeZone'
	Kabinet = models.ForeignKey(Kabinet_n_Outer, on_delete=models.CASCADE)
	ExcludeZone = models.ForeignKey(ExcludeZone, on_delete=models.CASCADE)

####################
# Пользовательские зоны
####################
class UserZone(models.Model):
	class Meta():
		db_table = "UserZone"
	UserZoneName = models.CharField(max_length=200, blank=True, null=True)
	User = models.ForeignKey(User, on_delete=models.CASCADE)
	LoadLandscape = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE)
	def __str__(self):
		return self.UserZoneName.encode('utf-8')

class VerticesUserZone(models.Model):
	class Meta():
		db_table = "VerticesUserZone"
	xCoord = models.FloatField()
	yCoord = models.FloatField()
	zmin = models.FloatField(blank=True, null=True)
	zmax = models.FloatField(blank=True, null=True)
	UserZone = models.ForeignKey(UserZone, on_delete=models.CASCADE)

class LoadLandscapeUserZone(models.Model):
	class Meta():
		db_table = "LoadLandscapeUserZone"
	LoadLandscape = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE)
	UserZone = models.ForeignKey(UserZone, on_delete=models.CASCADE)

class BuildingUserZone(models.Model):
	class Meta():
		db_table = "BuildingUserZone"
	Building = models.ForeignKey(Building, on_delete=models.CASCADE)
	UserZone = models.ForeignKey(UserZone, on_delete=models.CASCADE)

class FloorUserZone(models.Model):
	class Meta():
		db_table = "FloorUserZone"
	Floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
	UserZone = models.ForeignKey(UserZone, on_delete=models.CASCADE)

class KabinetUserZone(models.Model):
	class Meta():
		db_table = "KabinetUserZone"
	Kabinet = models.ForeignKey(Kabinet_n_Outer, on_delete=models.CASCADE)
	UserZone = models.ForeignKey(UserZone, on_delete=models.CASCADE)

class GroupUserZone(models.Model):
	class Meta():
		db_table = 'GroupUserZone'
	GroupName = models.CharField(max_length=200)
	GroupDescription = models.TextField()
	User = models.ForeignKey(User, on_delete=models.CASCADE)
	LoadLandscape = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE)
	def __str__(self):
		return self.GroupName.encode('utf-8')

class GroupUserZoneUserZone(models.Model):
	class Meta():
		db_table = 'GroupUserZoneUserZone'
	GroupUserZone = models.ForeignKey(GroupUserZone, on_delete=models.CASCADE)
	UserZone = models.ForeignKey(UserZone, on_delete=models.CASCADE)

class IncomeZoneUserZone(models.Model):
	class Meta():
		db_table = 'IncomeZoneUserZone'
	IncomeZone = models.ForeignKey(IncomeZone)
	UserZone = models.ForeignKey(UserZone)

class ExcludeZoneUserZone(models.Model):
	class Meta():
		db_table = 'ExcludeZoneUserZone'
	ExcludeZone = models.ForeignKey(ExcludeZone)
	UserZone = models.ForeignKey(UserZone)

############################
## Отчеты пользователей
############################
class TagFloorOrder(models.Model):
	class Meta():
		db_table = 'TagFloorOrder'
	Tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	Floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
	WriteTime = models.DateTimeField()

class TagKabinetOrder(models.Model):
	class Meta():
		db_table = 'TagKabinetOrder'
	Tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	Kabinet_n_Outer = models.ForeignKey(Kabinet_n_Outer, on_delete=models.CASCADE)
	WriteTime = models.DateTimeField()

class TagUzoneUserOrder(models.Model):
	class Meta():
		db_table = 'TagUzoneUserOrder'
	Tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	UserZone = models.ForeignKey(UserZone, on_delete=models.CASCADE)
	User = models.ForeignKey(User, on_delete=models.CASCADE)
	WriteTime = models.DateTimeField()

class TagOutOfBuilding(models.Model):
	class Meta():
		db_table = 'TagOutOfBuilding'
	Tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	WriteTime = models.DateTimeField()
	LoadLandscape = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE)

class TagNoUzone(models.Model):
	class Meta():
		db_table = 'TagNoUzone'
	Tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	User = models.ForeignKey(User, on_delete=models.CASCADE)
	WriteTime = models.DateTimeField()
	LoadLandscape = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE)
#########################
## Объекты
#########################

class ObjectType(models.Model):
	class Meta():
		db_table = 'ObjectType'
	Name = models.CharField(max_length=200, null=True, blank=True)
	Name_eng = models.CharField(max_length=200, null=True, blank=True)
	Command = models.CharField(max_length=200, null=True, blank=True)
	CommandList = models.CharField(max_length=200, null=True, blank=True)
	CommandDelete = models.CharField(max_length=200, null=True, blank=True)
	CommandUpdate = models.CharField(max_length=200, null=True, blank=True)
	def __str__(self):
		return self.Name.encode('utf-8')

class Object(models.Model):
	class Meta():
		db_table = 'Object'
	Name = models.CharField(max_length=200, null=True, blank=True)
	Description = models.TextField(null=True, blank=True)
	LoadLandscape = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE)
	xCoord = models.FloatField()
	yCoord = models.FloatField()
	zCoord = models.FloatField()
	server_id = models.CharField(max_length=200, null=True, blank=True)
	server_inUse = models.NullBooleanField(null=True)
	server_type = models.CharField(max_length=1, null=True, blank=True)
	server_radius = models.FloatField(null=True, blank=True)
	server_minNumPoints = models.IntegerField(null=True, blank=True)
	def __str__(self):
		if self.Name > 0:
			return self.Name.encode('utf-8')
		else:
			return 'нет наименования'

class ObjectObjectType(models.Model):
	class Meta():
		db_table = 'ObjectObjectType'
	ObjectType = models.ForeignKey(ObjectType, on_delete=models.CASCADE)
	Object = models.ForeignKey(Object, on_delete=models.CASCADE)

class ObjectBuilding(models.Model):
	class Meta():
		db_table = 'ObjectBuilding'
	Object = models.ForeignKey(Object, on_delete=models.CASCADE)
	Building = models.ForeignKey(Building, on_delete=models.CASCADE)

class ObjectFloor(models.Model):
	class Meta():
		db_table = 'ObjectFloor'
	Object = models.ForeignKey(Object, on_delete=models.CASCADE)
	Floor = models.ForeignKey(Floor, on_delete=models.CASCADE)

class ObjectKabinet(models.Model):
	class Meta():
		db_table = 'ObjectKabinet'
	Object = models.ForeignKey(Object, on_delete=models.CASCADE)
	Kabinet = models.ForeignKey(Kabinet_n_Outer, on_delete=models.CASCADE)
#########################
###sessions
#########################
class SessionTable(models.Model):
	class Meta():
		db_table = 'SessionTable'
	LoadLandscape = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE)
	idLayer = models.IntegerField(blank=True, null=True)
	inuse = models.NullBooleanField(blank=True, null=True)
	name = models.CharField(max_length=200, blank=True, null=True)
	server_id = models.IntegerField(blank=True, null=True)
	server_idLayer = models.IntegerField(blank=True, null=True)

class SessionLayer(models.Model):
	class Meta():
		db_table = 'SessionLayer'
	SessionTable = models.ForeignKey(SessionTable, on_delete=models.CASCADE)
	height1 = models.FloatField(blank=True, null=True)
	height2 = models.FloatField(blank=True, null=True)
	ws_id = models.IntegerField(blank=True, null=True)
	latitude1 = models.FloatField(blank=True, null=True)
	latitude2 = models.FloatField(blank=True, null=True)
	longitude1 = models.FloatField(blank=True, null=True)
	longitude2 = models.FloatField(blank=True, null=True)
	name = models.CharField(max_length=200, blank=True, null=True)
	scaleX = models.FloatField(blank=True, null=True)
	scaleY = models.FloatField(blank=True, null=True)
	x1 = models.FloatField(blank=True, null=True)
	x2 = models.FloatField(blank=True, null=True)
	y1 = models.FloatField(blank=True, null=True)
	y2 = models.FloatField(blank=True, null=True)
	z1 = models.FloatField(blank=True, null=True)
	z2 = models.FloatField(blank=True, null=True)
	server_id = models.IntegerField(blank=True, null=True)

class SessionPlan(models.Model):
	class Meta():
		db_table = 'SessionPlan'
	SessionTable = models.ForeignKey(SessionTable, on_delete=models.CASCADE)
	ws_id = models.IntegerField(blank=True, null=True)
	name = models.CharField(max_length=200, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	x = models.FloatField(blank=True, null=True)
	y = models.FloatField(blank=True, null=True)
	z = models.FloatField(blank=True, null=True)
	sizeX = models.FloatField(blank=True, null=True)
	sizeY = models.FloatField(blank=True, null=True)
	sizeZ = models.FloatField(blank=True, null=True)
	angleRotateX = models.FloatField(blank=True, null=True)	
	angleRotateY = models.FloatField(blank=True, null=True)
	angleRotateZ = models.FloatField(blank=True, null=True)
	objType = models.FloatField(blank=True, null=True)
	server_id = models.IntegerField(blank=True, null=True)

class SessionPlanTree(models.Model):
	class Meta():
		db_table = 'SessionPlanTree'
	SessionTable = models.ForeignKey(SessionTable, on_delete=models.CASCADE)
	ws_id = models.IntegerField(blank=True, null=True)
	server_id = models.IntegerField(blank=True, null=True)
	ws_parent_id = models.IntegerField(blank=True, null=True)
	server_parent_id = models.IntegerField(blank=True, null=True)

class Command(models.Model):
	class Meta():
		db_table = 'Command'
	Name = models.CharField(max_length=200, blank=True, null=True)
	def __str__(self):
		return self.Name.encode('utf-8')

#####################
## CalibrationPoints
######################
class Cpoint(models.Model):
	class Meta():
		db_table = 'Cpoint'
	Name = models.CharField(max_length=200, blank=True, null=True)
	xCoord = models.FloatField(blank=True, null=True)
	yCoord = models.FloatField(blank=True, null=True)
	zCoord = models.FloatField(blank=True, null=True)
	LoadLandscape = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE)
	def __str__(self):
		return self.Name.encode('utf-8')

class PointBuilding(models.Model):
	class Meta():
		db_table = 'PointBuilding'
	Cpoint = models.ForeignKey(Cpoint, on_delete=models.CASCADE)
	Building = models.ForeignKey(Building, on_delete=models.CASCADE)

class PointFloor(models.Model):
	class Meta():
		db_table = 'PointFloor'
	Cpoint = models.ForeignKey(Cpoint, on_delete=models.CASCADE)
	Floor = models.ForeignKey(Floor, on_delete=models.CASCADE)

class PointKabinet(models.Model):
	class Meta():
		db_table = 'PointKabinet'
	Cpoint = models.ForeignKey(Cpoint, on_delete=models.CASCADE)
	Kabinet = models.ForeignKey(Kabinet_n_Outer, on_delete=models.CASCADE)

class PointBeenCalibrated(models.Model):
	class Meta():
		db_table = 'PointBeenCalibrated'
	Cpoint = models.ForeignKey(Cpoint)
	Date = models.DateTimeField()
##############################
# запросы
##############################
class Query(models.Model):
	class Meta():
		db_table = 'Query'
	Name = models.CharField(max_length=200, blank=True, null=True)
	Parameters = jsonfield.JSONField(null=True, blank=True)
	def __str__(self):
		return self.Name.encode('utf-8')

# параметры для запросов
class Qparameter(models.Model):
	class Meta():
		db_table = 'Qparameter'
	Name = models.CharField(max_length=200, blank=True, null=True)
	KeyName = models.CharField(max_length=50, blank=True, null=True)
	def __str__(self):
		return self.Name.encode('utf-8')

#связь параметры - запросы
class QueryQparameter(models.Model):
	class Meta():
		db_table = 'QueryQparameter'
	Query = models.ForeignKey(Query, on_delete=models.CASCADE)
	Qparameter = models.ForeignKey(Qparameter, on_delete=models.CASCADE)
	def __str__(self):
		return self.Query.Name.encode('utf-8')