# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-10 11:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0052_auto_20160310_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='building',
            name='Color',
        ),
        migrations.RemoveField(
            model_name='floor',
            name='Color',
        ),
        migrations.RemoveField(
            model_name='kabinet_n_outer',
            name='Color',
        ),
        migrations.RemoveField(
            model_name='loadlandscape',
            name='Color',
        ),
        migrations.RemoveField(
            model_name='wall',
            name='Color',
        ),
    ]
