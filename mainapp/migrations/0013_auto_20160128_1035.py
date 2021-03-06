# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-28 07:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_std0_timedelta'),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BuildingName', models.CharField(max_length=200, null=True)),
                ('dae_BuildingName', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'Building',
            },
        ),
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FloorName', models.CharField(max_length=200, null=True)),
                ('dae_FloorName', models.CharField(max_length=200)),
                ('Building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Building')),
            ],
            options={
                'db_table': 'Floor',
            },
        ),
        migrations.CreateModel(
            name='Kabinet_n_Outer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Kabinet_n_OuterName', models.CharField(max_length=200, null=True)),
                ('dae_Kabinet_n_OuterName', models.CharField(max_length=200)),
                ('Floor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Floor')),
            ],
            options={
                'db_table': 'Kabinet_n_Outer',
            },
        ),
        migrations.CreateModel(
            name='LoadLandscape',
            fields=[
                ('landscape_name', models.CharField(max_length=100)),
                ('landscape_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('landscape_source', models.FileField(blank=True, null=True, upload_to=b'static/js/webgl/models/')),
            ],
            options={
                'db_table': 'LoadLandscape',
            },
        ),
        migrations.CreateModel(
            name='Wall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('WallName', models.CharField(max_length=200, null=True)),
                ('dae_WallName', models.CharField(max_length=200)),
                ('Kabinet_n_Outer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Kabinet_n_Outer')),
                ('LoadLandscape', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.LoadLandscape')),
            ],
            options={
                'db_table': 'Wall',
            },
        ),
        migrations.AddField(
            model_name='kabinet_n_outer',
            name='LoadLandscape',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.LoadLandscape'),
        ),
        migrations.AddField(
            model_name='floor',
            name='LoadLandscape',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.LoadLandscape'),
        ),
        migrations.AddField(
            model_name='building',
            name='LoadLandscape',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.LoadLandscape'),
        ),
    ]
