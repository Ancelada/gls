#!/usr/bin/python
# -*- coding: utf8 -*-
from django.db import models

# Create your models here.

class Metka(models.Model):
	class Meta():
		db_table = 'Metka'
	text = models.CharField(max_length=200)

# СООБЩЕНИЯ

# типы данных
class DataType(models.Model):
	class Meta():
		db_table = 'DataType'
	DataTypeName = models.CharField(max_length=200)
	DjangoFormat = models.CharField(max_length=200)
	def __str__(self):
		return self.DataTypeName.encode('utf-8')
# конец типы данных


# сообщения с определениями полей
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

# тип формата определения сообщений местонахождения
class LMDM_Format(models.Model):
	class Meta():
		db_table = 'LMDM_Format'
	LMDM_FormatName = models.CharField(max_length=200)
	def __str__(self):
		return self.LMDM_FormatName.encode('utf-8')
# конец типа формата определения сообщений местонахождения

# сообщения с oпределениями формата сообщений местонахождения
class Locate_Message_Definition_Message(models.Model):
	class Meta():
		db_table = 'Locate_Message_Definition_Message'
	Source = models.CharField(max_length=200)
	Format = models.ForeignKey(LMDM_Format)
# конец сообщения с определениями формата сообщений местонахождения

# КОНЕЦ СООБЩЕНИЯ