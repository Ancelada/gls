# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-12 11:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_metka_dateimport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='std0',
            name='Timestamp',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
