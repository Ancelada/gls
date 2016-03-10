#!/usr/bin/python
# -*- coding: utf8 -*-
from django.contrib import admin
from mainapp.models import *
# СООБЩЕНИЯ

# типы данных
class DataTypeAdmin(admin.ModelAdmin):
	fieldsets = [
		('Наименование', {'fields': ['DataTypeName']}),
		('Наименование в Джанго', {'fields': ['DjangoFormat']}),
	]
# сообщения с определениями полей
class Field_Definition_MessageAdmin(admin.ModelAdmin):
	fieldsets = [
		('Наименование', {'fields': ['Field_Definition_MessageName']}),
		('Xml-тэг', {'fields': ['XmlTag']}),
		('Тип данных', {'fields': ['DataType']}),
		('Минимально символов', {'fields': ['LengthMin']}),
		('Максимально символов', {'fields': ['LengthMax']}),
	]
# тип формата определения сообщений местонахождения
class LMDMFormatAdmin(admin.ModelAdmin):
	fieldsets = [
		('Наименование', {'fields': ['LMDMFormatName']}),
	]
# сообщения с oпределениями формата сообщений местонахождения
class Locate_Message_Definition_MessageAdmin(admin.ModelAdmin):
	fieldsets = [
		('Источник', {'fields': ['Source']}),
		('Тип формата', {'fields': ['Format']}),
	]
admin.site.register(DataType, DataTypeAdmin)
admin.site.register(Field_Definition_Message, Field_Definition_MessageAdmin)
admin.site.register(LMDMFormat, LMDMFormatAdmin)
admin.site.register(Locate_Message_Definition_Message, Locate_Message_Definition_MessageAdmin)

#TagType
class TagTypeAdmin(admin.ModelAdmin):
	fieldsets = [
		('Наименование', {'fields': ['Name']}),
	]
admin.site.register(TagType, TagTypeAdmin)
