# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-15 04:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0017_auto_20160215_0739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loadlandscape',
            name='landscape_source',
            field=models.FileField(blank=True, null=True, upload_to=b'static/js/webgl/models/<function get_upload_file_name at 0xb655e9cc>'),
        ),
    ]
