# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-29 15:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0167_sessiontable_loadlandscape'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sessiontable',
            name='LoadLandscape2',
        ),
    ]