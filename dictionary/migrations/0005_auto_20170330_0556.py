# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-30 10:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0004_auto_20170328_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='simple',
            field=models.CharField(max_length=255),
        ),
    ]