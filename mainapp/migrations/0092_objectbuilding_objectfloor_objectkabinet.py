# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-25 17:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0091_objecttype_commanddelete'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectBuilding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Building')),
                ('Object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Object')),
            ],
            options={
                'db_table': 'ObjectBuilding',
            },
        ),
        migrations.CreateModel(
            name='ObjectFloor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Floor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Floor')),
                ('Object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Object')),
            ],
            options={
                'db_table': 'ObjectFloor',
            },
        ),
        migrations.CreateModel(
            name='ObjectKabinet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Kabinet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Kabinet_n_Outer')),
                ('Object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Object')),
            ],
            options={
                'db_table': 'ObjectKabinet',
            },
        ),
    ]