# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-12 14:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0171_tagnode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='node',
            old_name='description',
            new_name='Description',
        ),
        migrations.RenameField(
            model_name='node',
            old_name='name',
            new_name='Name',
        ),
    ]
