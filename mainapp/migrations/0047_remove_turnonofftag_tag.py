# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-08 18:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0046_remove_tag_taggroup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turnonofftag',
            name='Tag',
        ),
    ]
