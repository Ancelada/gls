# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-16 08:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0058_auto_20160315_0912'),
    ]

    operations = [
        migrations.AddField(
            model_name='verticesincomezone',
            name='zmax',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='verticesincomezone',
            name='zmin',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
