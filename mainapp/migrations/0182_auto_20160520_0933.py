# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-20 09:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0181_auto_20160518_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tagnode',
            name='Node',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.Node'),
        ),
        migrations.AlterField(
            model_name='tagnode',
            name='Tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.Tag'),
        ),
    ]
