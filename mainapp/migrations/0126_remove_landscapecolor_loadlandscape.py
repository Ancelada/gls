# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-29 13:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0125_landscapecolor_loadlandscape2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='landscapecolor',
            name='LoadLandscape',
        ),
    ]
