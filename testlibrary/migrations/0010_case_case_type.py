# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-28 21:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testlibrary', '0009_auto_20161028_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='case_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='testlibrary.CaseType'),
        ),
    ]