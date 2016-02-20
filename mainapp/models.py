#!/usr/bin/python
# -*- coding: utf8 -*-
from django.db import models
from django.conf import settings

def get_upload_file_name(instance, filename):
	return '%s_%s' % (str(time).replace('.', '_'), filename)

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
	landscape_source = models.FileField(upload_to='static/js/webgl/models/', blank=True, null=True)
	# landscape_source = models.FileField(upload_to='static/js/webgl/models/%s' % get_upload_file_name, blank=True, null=True)

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
	LoadLandscape = models.ForeignKey(LoadLandscape)

class VerticesBuilding(models.Model):
	class Meta():
		db_table = 'VerticesBuilding'
	x = models.FloatField(null=True)
	y = models.FloatField(null=True)
	Building = models.ForeignKey(Building, on_delete=models.CASCADE)
	LoadLandscape = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE, null=True)

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
	LoadLandscape = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE, null=True)

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
	LoadLandscape = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE, null=True)

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
### Метки
######################

class Tag(models.Model):
	class Meta():
		db_table = 'Tag'
	TagId = models.CharField(primary_key=True, max_length=20)
	TagType = models.CharField(max_length=20, null=True)
	Group = models.CharField(max_length=20, null=True)
	Name = models.CharField(max_length=200, null=True)

######################
### События
######################

class ZoneChange(models.Model):
	class Meta():
		db_table = 'ZoneChange'
	Tag = models.ForeignKey(Tag)
	ZoneNew = models.ForeignKey(LoadLandscape, on_delete=models.CASCADE)
	ChangeTime = models.DateTimeField(null=True)


class BldChange(models.Model):
	class Meta():
		db_table = 'BldChange'
	Tag = models.ForeignKey(Tag)
	BldNew = models.ForeignKey(Building, on_delete=models.CASCADE)
	ChangeTime = models.DateTimeField(null=True)

class FlrChange(models.Model):
	class Meta():
		db_table = 'FlrChange'
	Tag = models.ForeignKey(Tag)
	FlrNew = models.ForeignKey(Floor, on_delete=models.CASCADE)
	ChangeTime = models.DateTimeField(null=True)

class KbntChange(models.Model):
	class Meta():
		db_table = 'KbntChange'
	Tag = models.ForeignKey(Tag)
	KbntNew = models.ForeignKey(Kabinet_n_Outer, on_delete=models.CASCADE)
	ChangeTime = models.DateTimeField(null=True)