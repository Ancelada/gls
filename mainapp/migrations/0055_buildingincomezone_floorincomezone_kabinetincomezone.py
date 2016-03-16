# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-11 09:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0054_buildingcolor_floorcolor_kabinetcolor_landscapecolor'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingIncomeZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Building')),
            ],
            options={
                'db_table': 'BuildingIncomeZone',
            },
        ),
        migrations.CreateModel(
            name='FloorIncomeZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Floor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Floor')),
            ],
            options={
                'db_table': 'FloorIncomeZone',
            },
        ),
        migrations.CreateModel(
            name='KabinetIncomeZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Kabinet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Kabinet_n_Outer')),
            ],
            options={
                'db_table': 'KabinetIncomeZone',
            },
        ),
    ]