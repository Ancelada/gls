#!/usr/bin/python
# -*- coding: utf8 -*-
from django.db import models

# Create your models here.

class Metka(models.Model):
	class Meta():
		db_table = 'Metka'
	text = models.TextField()

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
	Timestamp = models.CharField(max_length=10, null=True)
	Status = models.CharField(max_length=1, null=True)
	Session = models.CharField(max_length=8, null=True)
	Zone = models.CharField(max_length=200, null=True)
	DateImport = models.DateTimeField(auto_now=True, null=True)

######################## конец записи сообщений по форматам: ############################

###################
# КОНЕЦ СООБЩЕНИЯ SLMP
###################