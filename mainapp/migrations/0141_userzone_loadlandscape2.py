# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-29 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0140_remove_turnonofftag_loadlandscape2'),
    ]

    operations = [
        migrations.AddField(
            model_name='userzone',
            name='LoadLandscape2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
