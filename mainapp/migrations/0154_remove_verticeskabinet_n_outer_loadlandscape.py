# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-29 14:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0153_verticeskabinet_n_outer_loadlandscape2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='verticeskabinet_n_outer',
            name='LoadLandscape',
        ),
    ]
