# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-28 11:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0002_auto_20170326_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='pronunciation',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='entry',
            name='simple',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='entry',
            name='traditional',
            field=models.CharField(max_length=255),
        ),
    ]