# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-25 11:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20151225_0912'),
    ]

    operations = [
        migrations.CreateModel(
            name='Std0',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LocateMessageDefinition', models.CharField(max_length=200)),
                ('LabD', models.CharField(max_length=200)),
                ('Std0', models.CharField(max_length=200)),
                ('Tag_ID_Format', models.CharField(max_length=200)),
                ('Tag_ID', models.CharField(max_length=200)),
                ('X', models.IntegerField()),
                ('Y', models.IntegerField()),
                ('Z', models.IntegerField()),
                ('Battery', models.IntegerField()),
                ('Timestamp', models.CharField(max_length=10)),
                ('Status', models.CharField(max_length=1)),
                ('Session', models.CharField(max_length=8)),
                ('Zone', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'Std0',
            },
        ),
    ]