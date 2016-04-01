# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-30 11:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0062_auto_20160317_0852'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingUserZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Building')),
            ],
            options={
                'db_table': 'BuildingUserZone',
            },
        ),
        migrations.CreateModel(
            name='FloorUserZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Floor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Floor')),
            ],
            options={
                'db_table': 'FloorUserZone',
            },
        ),
        migrations.CreateModel(
            name='GroupUserZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GroupName', models.CharField(max_length=200)),
                ('GroupDescription', models.TextField()),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'GroupUserZone',
            },
        ),
        migrations.CreateModel(
            name='GroupUserZoneUserZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GroupUserZone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.GroupUserZone')),
            ],
            options={
                'db_table': 'GroupUserZoneUserZone',
            },
        ),
        migrations.CreateModel(
            name='KabinetUzerZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Kabinet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Kabinet_n_Outer')),
            ],
            options={
                'db_table': 'KabinetUzerZone',
            },
        ),
        migrations.CreateModel(
            name='LoadLandscapeUserZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LoadLandscape', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.LoadLandscape')),
            ],
            options={
                'db_table': 'LoadLandscapeUserZone',
            },
        ),
        migrations.CreateModel(
            name='UserZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'UserZone',
            },
        ),
        migrations.CreateModel(
            name='VerticesUserZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xCoord', models.FloatField()),
                ('yCoord', models.FloatField()),
                ('zmin', models.FloatField(blank=True, null=True)),
                ('zmax', models.FloatField(blank=True, null=True)),
                ('UserZone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.UserZone')),
            ],
            options={
                'db_table': 'VerticesUserZone',
            },
        ),
        migrations.AddField(
            model_name='loadlandscapeuserzone',
            name='UserZone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.UserZone'),
        ),
        migrations.AddField(
            model_name='kabinetuzerzone',
            name='UserZone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.UserZone'),
        ),
        migrations.AddField(
            model_name='groupuserzoneuserzone',
            name='UserZone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.UserZone'),
        ),
        migrations.AddField(
            model_name='flooruserzone',
            name='UzerZone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.UserZone'),
        ),
        migrations.AddField(
            model_name='buildinguserzone',
            name='UserZone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.UserZone'),
        ),
    ]