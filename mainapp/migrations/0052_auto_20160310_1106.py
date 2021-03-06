# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-10 11:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0051_tag_tagtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='Color',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='floor',
            name='Color',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='kabinet_n_outer',
            name='Color',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loadlandscape',
            name='Color',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='wall',
            name='Color',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
