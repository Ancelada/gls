# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-29 13:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0123_kabinet_n_outer_loadlandscape'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kabinet_n_outer',
            name='LoadLandscape2',
        ),
    ]
