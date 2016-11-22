# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-22 17:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testlibrary', '0015_auto_20161122_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='testrun',
            name='test_results',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='testlibrary.TestResult'),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='start_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='testrun',
            name='test_cases',
            field=models.ManyToManyField(to='testlibrary.Case'),
        ),
    ]