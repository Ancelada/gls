# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-12 13:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0005_auto_20160411_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameter',
            name='domName',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
