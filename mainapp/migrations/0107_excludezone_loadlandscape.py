# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-29 13:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0106_remove_excludezone_loadlandscape'),
    ]

    operations = [
        migrations.AddField(
            model_name='excludezone',
            name='LoadLandscape',
            field=models.ForeignKey(default='0000', on_delete=django.db.models.deletion.CASCADE, to='mainapp.LoadLandscape'),
            preserve_default=False,
        ),
    ]
