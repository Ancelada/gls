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

class ObjectTypeAdmin(admin.ModelAdmin):
	fieldsets = [
		('Наименование', {'fields': ['Name']}),
		('Наименование_анг', {'fields': ['Name_eng']}),
		('Command', {'fields': ['Command']}),
		('CommandList', {'fields': ['CommandList']}),
		('CommandDelete', {'fields': ['CommandDelete']}),
		('CommandUpdate', {'fields': ['CommandUpdate']}),
	]

class ObjectAdmin(admin.ModelAdmin):
	fieldsets = [
		('Наименование', {'fields': ['Name']}),
		('Описание', {'fields': ['Description']}),
		('Сцена', {'fields': ['LoadLandscape'] }),
		('x', {'fields': ['xCoord']}),
		('y', {'fields': ['yCoord']}),
		('z', {'fields': ['zCoord']}),
	]
class CommandAdmin(admin.ModelAdmin):
	fieldsets = [
		('Наименование', {'fields': ['Name']}),
	]
admin.site.register(Command, CommandAdmin)
admin.site.register(Object, ObjectAdmin)
admin.site.register(ObjectType, ObjectTypeAdmin)
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

#Node
class NodeAdmin(admin.ModelAdmin):
	fieldsets = [
		('Наименование', {'fields': ['Name']}),
		('Описание', {'fields': ['Description']})
	]
admin.site.register(Node, NodeAdmin)

#TagNode
class TagNodeAdmin(admin.ModelAdmin):
	fieldsets = [
		('Tag', {'fields': ['Tag']}),
		('Node', {'fields': ['Node']})
	]
admin.site.register(TagNode, TagNodeAdmin)

#Tag
class TagAdmin(admin.ModelAdmin):
	fieldsets = [
		('Идентификатор', {'fields': ['TagId']}),
		('Наименование', {'fields': ['Name']}),
		('Тип тега', {'fields': ['TagType']}),
	]
admin.site.register(Tag, TagAdmin)

#LocationMethods
class LocationMethodsAdmin(admin.ModelAdmin):
	fieldsets = [
		('Наименование параметра', {'fields': ['ParameterName']}),
	]
admin.site.register(LocationMethods, LocationMethodsAdmin)

#Sensors
class SensorsAdmin(admin.ModelAdmin):
	fieldsets = [
		('Наименование параметра', {'fields': ['ParameterName']}),
	]
admin.site.register(Sensors, SensorsAdmin)

#TimeUpdateLocation
class TimeUpdateLocationAdmin(admin.ModelAdmin):
	fieldsets = [
		('Наименование параметра', {'fields': ['ParameterName']}),
	]
admin.site.register(TimeUpdateLocation, TimeUpdateLocationAdmin)

#CorrectionFilter
class CorrectionFilterAdmin(admin.ModelAdmin):
	fieldsets = [
		('Наименование параметра', {'fields': ['ParameterName']}),
		('Тип значения параметра', {'fields': ['ParameterValueType']}),
	]
admin.site.register(CorrectionFilter, CorrectionFilterAdmin)

#Query
class QueryAdmin(admin.ModelAdmin):
	fieldsets = [
		('Наименование запроса', {'fields': ['Name']}),
		('Параметры', {'fields': ['Parameters']})
	]
admin.site.register(Query, QueryAdmin)

#Qparameter
class QparameterAdmin(admin.ModelAdmin):
	fieldsets = [
		('Наименование параметра', {'fields': ['Name']}),
		('Ключ параметра', {'fields': ['KeyName']})
	]
admin.site.register(Qparameter, QparameterAdmin)

#QueryParameter
class QueryQparameterAdmin(admin.ModelAdmin):
	fieldsets = [
		('связь Query', {'fields': ['Query']}),
		('связь Parameter', {'fields': ['Qparameter']})
	]
admin.site.register(QueryQparameter, QueryQparameterAdmin)