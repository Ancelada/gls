#!/usr/bin/python
# -*- coding: utf8 -*-
from django.contrib import admin
from report.models import *
class ReportAdmin(admin.ModelAdmin):
	fieldsets = [
		('Наименование', {'fields': ['Name']}),
		('Описание', {'fields': ['Description']}),
		('Может быть множество меток', {'fields': ['CanBeMultipleTagId']}),
	]
class ReportUserAdmin(admin.ModelAdmin):
	fieldsets = [
		('Пользователь', {'fields': ['User']}),
		('Отчет', {'fields': ['Report']}),
	]
class ReportParameterAdmin(admin.ModelAdmin):
	fieldsets = [
		('Параметр', {'fields': ['Parameter']}),
		('Отчет', {'fields': ['Report']}),
	]
class ParameterAdmin(admin.ModelAdmin):
	fieldsets = [
		('Наименование', {'fields': ['Name']}),
		('dom наименование', {'fields': ['domName']}),
	]
# Register your models here.
admin.site.register(Report, ReportAdmin)
admin.site.register(ReportUser, ReportUserAdmin)
admin.site.register(ReportParameter, ReportParameterAdmin)
admin.site.register(Parameter, ParameterAdmin)