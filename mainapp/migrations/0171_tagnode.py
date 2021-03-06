# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-12 14:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0170_node'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Node')),
                ('Tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Tag')),
            ],
            options={
                'db_table': 'TagNode',
            },
        ),
    ]
