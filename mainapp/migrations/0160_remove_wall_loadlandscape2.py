# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-29 15:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0159_wall_loadlandscape'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wall',
            name='LoadLandscape2',
        ),
    ]
