# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-16 11:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0176_auto_20160516_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='Registred',
            field=models.NullBooleanField(),
        ),
    ]