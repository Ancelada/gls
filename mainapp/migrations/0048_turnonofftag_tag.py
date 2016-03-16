# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-08 18:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0047_remove_turnonofftag_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='turnonofftag',
            name='Tag',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mainapp.Tag'),
            preserve_default=False,
        ),
    ]