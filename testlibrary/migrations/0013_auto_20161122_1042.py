# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-22 16:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testlibrary', '0012_testresult_testrun'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date published'),
        ),
    ]
