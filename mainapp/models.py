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
	landscape_source = models.FileField(upload_to='static/js/webgl/models/%s' % get_upload_file_name, blank=True, null=True)

class Building(models.Model):
	class Meta():
		db_table = 'Building'
	BuildingName = models.CharField(max_length=200, null=True)
	dae_BuildingName = models.CharField(max_length=200)
	LoadLandscape = models.ForeignKey(LoadLandscape)

class Floor(models.Model):
	class Meta():
		db_table = 'Floor'
	FloorName = models.CharField(max_length=200, null=True)
	dae_FloorName = models.CharField(max_length=200)
	Building = models.ForeignKey(Building)
	LoadLandscape = models.ForeignKey(LoadLandscape)

class Kabinet_n_Outer(models.Model):
	class Meta():
		db_table = 'Kabinet_n_Outer'
	Kabinet_n_OuterName = models.CharField(max_length=200, null=True)
	dae_Kabinet_n_OuterName = models.CharField(max_length=200)
	Floor = models.ForeignKey(Floor)
	LoadLandscape = models.ForeignKey(LoadLandscape)

class Wall(models.Model):
	class Meta():
		db_table = 'Wall'
	WallName = models.CharField(max_length=200, null=True)
	dae_WallName = models.CharField(max_length=200)
	Kabinet_n_Outer = models.ForeignKey(Kabinet_n_Outer)
	LoadLandscape = models.ForeignKey(LoadLandscape)

####################
##SockJs
####################
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

class Order(models.Model):
	class Meta():
		db_table = 'Order'
	OrderName = models.CharField(max_length=200, null=True)

	def lock(self):
		print "added"
		if self.OrderName != '':
			service_queue('order_lock', json({
				'user': self.client.pk,
				'order': self.pk,	
			}))

	def done(self):
		print "added"
		if self.OrderName != '':
			service_queue('order_done', json({
				'user': self.client.pk,
				'order': self.pk,	
			}))