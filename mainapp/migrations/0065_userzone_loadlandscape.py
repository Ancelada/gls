# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-31 08:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0064_userzone_userzonename'),
    ]

    operations = [
        migrations.AddField(
            model_name='userzone',
            name='LoadLandscape',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mainapp.LoadLandscape'),
            preserve_default=False,
        ),
    ]