# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-18 15:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0180_point_pointbuilding_pointfloor_pointkabinet'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Point',
            new_name='Cpoint',
        ),
        migrations.RenameField(
            model_name='pointbuilding',
            old_name='Point',
            new_name='Cpoint',
        ),
        migrations.RenameField(
            model_name='pointfloor',
            old_name='Point',
            new_name='Cpoint',
        ),
        migrations.RenameField(
            model_name='pointkabinet',
            old_name='Point',
            new_name='Cpoint',
        ),
        migrations.AlterModelTable(
            name='cpoint',
            table='Cpoint',
        ),
    ]
