# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-15 05:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0027_auto_20160215_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='LoadLandscape',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.LoadLandscape'),
        ),
    ]
