#!/usr/bin/python
# -*- coding: utf8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import jsonfield
# Create your models here.

class Report(models.Model):
	class Meta():
		db_table = 'Report'
	Name = models.CharField(max_length=200, blank=True, null=True)
	Description = models.TextField()
	CanBeMultipleTagId = models.BooleanField()
	def __str__(self):
		return self.Name.encode('utf-8')

class ReportUser(models.Model):
	class Meta():
		db_table = 'ReportUser'
	User = models.ForeignKey(User, on_delete=models.CASCADE)
	Report = models.ForeignKey(Report, on_delete=models.CASCADE)

class Parameter(models.Model):
	class Meta():
		db_table = 'Parameter'
	Name = models.CharField(max_length=200, blank=True, null=True)
	domName = models.CharField(max_length=200, blank=True, null=True)
	def __str__(self):
		return self.Name.encode('utf-8')

class ReportParameter(models.Model):
	class Meta():
		db_table = 'ReportParameter'
	Parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
	Report = models.ForeignKey(Report, on_delete=models.CASCADE)