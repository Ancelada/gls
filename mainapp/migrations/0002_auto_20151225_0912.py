# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-25 06:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LMDM_Format',
            new_name='LMDMFormat',
        ),
        migrations.RenameField(
            model_name='lmdmformat',
            old_name='LMDM_FormatName',
            new_name='LMDMFormatName',
        ),
    ]