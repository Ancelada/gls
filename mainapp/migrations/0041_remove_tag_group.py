# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-03 08:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0040_auto_20160303_0840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='Group',
        ),
    ]
