# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-04 09:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_std0'),
    ]

    operations = [
        migrations.AddField(
            model_name='std0',
            name='DateImport',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 1, 4, 9, 29, 6, 510294, tzinfo=utc)),
            preserve_default=False,
        ),
    ]