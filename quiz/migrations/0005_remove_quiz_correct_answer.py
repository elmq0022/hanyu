# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-24 03:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20170520_1844'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='correct_answer',
        ),
    ]
