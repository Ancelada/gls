# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-29 15:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0164_remove_object_loadlandscape2'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessiontable',
            name='LoadLandscape2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
