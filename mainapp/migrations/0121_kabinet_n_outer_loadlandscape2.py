# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-29 13:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0120_remove_incomezone_loadlandscape2'),
    ]

    operations = [
        migrations.AddField(
            model_name='kabinet_n_outer',
            name='LoadLandscape2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
