# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-06 19:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0044_taggroup_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='taggroup_tag',
            name='User',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
