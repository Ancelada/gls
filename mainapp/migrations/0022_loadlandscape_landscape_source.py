# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-15 04:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0021_remove_loadlandscape_landscape_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='loadlandscape',
            name='landscape_source',
            field=models.FileField(blank=True, null=True, upload_to=b'static/js/webgl/models/<function get_upload_file_name at 0xb656d844>'),
        ),
    ]
