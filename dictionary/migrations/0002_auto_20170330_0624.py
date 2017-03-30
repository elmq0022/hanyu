# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-30 11:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='id',
        ),
        migrations.AlterField(
            model_name='entry',
            name='order',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
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