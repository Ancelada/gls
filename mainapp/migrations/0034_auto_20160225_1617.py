# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-25 16:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0033_auto_20160225_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='loadlandscape',
            name='controls_target_x',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='loadlandscape',
            name='controls_target_y',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='loadlandscape',
            name='controls_target_z',
            field=models.FloatField(null=True),
        ),
    ]