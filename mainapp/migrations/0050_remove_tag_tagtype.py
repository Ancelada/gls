# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-09 10:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0049_tagtype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='TagType',
        ),
    ]