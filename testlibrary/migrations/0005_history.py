# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-27 16:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testlibrary', '0004_release'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision_number', models.IntegerField()),
            ],
        ),
    ]