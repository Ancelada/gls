#!/usr/bin/python
# -*- coding: utf8 -*-
from django.contrib import admin
from mainapp.models import Field_Definition_Message, DataType
from mainapp.models import LMDM_Format, Locate_Message_Definition_Message
# СООБЩЕНИЯ

# типы данных

class DataTypeAdmin(admin.ModelAdmin):
	fieldsets = [
		('Наименование', {'fields': ['DataTypeName']}),
		('Наименование в Джанго', {'fields': ['DjangoFormat']}),
	]
admin.site.register(DataType, DataTypeAdmin)
# конец типы данных

# сообщения с определениями полей

class Field_Definition_MessageAdmin(admin.ModelAdmin):
	fieldsets = [
		('Наименование', {'fields': ['Field_Definition_MessageName']}),
		('Xml-тэг', {'fields': ['XmlTag']}),
		('Тип данных', {'fields': ['DataType']}),
		('Минимально символов', {'fields': ['LengthMin']}),
		('Максимально символов', {'fields': ['LengthMax']}),
	]

admin.site.register(Field_Definition_Message, Field_Definition_MessageAdmin)
# конец сообщений с определениями полей

# тип формата определения сообщений местонахождения
class LMDM_FormatAdmin(admin.ModelAdmin):
	fieldsets = [
		('Наименование', {'fields': ['LMDM_FormatName']}),
	]
# конец типа формата определения сообщений местонахождения

# сообщения с oпределениями формата сообщений местонахождения
class Locate_Message_Definition_Message(admin.ModelAdmin):
	fieldsets = [
		('Источник', {'fields': ['Source']}),
		('Тип формата', {'fields': ['Format']}),
	]
# конец сообщения с определениями формата сообщений местонахождения

# КОНЕЦ СООБЩЕНИЯ