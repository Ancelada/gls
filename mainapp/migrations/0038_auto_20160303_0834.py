# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-03 08:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0037_taggroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taggroup',
            name='CircleColor',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='taggroup',
            name='GeometryMeshesColor',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='taggroup',
            name='GeometryMeshesSize',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='taggroup',
            name='GeometryMeshesType',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='taggroup',
            name='GroupName',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
