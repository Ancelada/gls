# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-29 14:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0146_remove_verticesfloor_loadlandscape'),
    ]

    operations = [
        migrations.AddField(
            model_name='verticesfloor',
            name='LoadLandscape',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.LoadLandscape'),
        ),
    ]
