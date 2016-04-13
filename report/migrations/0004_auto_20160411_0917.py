# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-11 09:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0003_auto_20160411_0910'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='reportparameter',
            name='Name',
        ),
        migrations.AddField(
            model_name='reportparameter',
            name='Parameter',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='report.Parameter'),
            preserve_default=False,
        ),
    ]
