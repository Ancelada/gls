# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-03 08:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0039_tag_taggroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='TagGroup',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mainapp.TagGroup'),
            preserve_default=False,
        ),
    ]
