# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-27 23:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testlibrary', '0007_auto_20161027_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='case_version',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='testlibrary.CaseHistory'),
        ),
    ]
