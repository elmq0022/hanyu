# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-29 15:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning_tools', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='word',
            old_name='count_type',
            new_name='learning_status',
        ),
        migrations.RemoveField(
            model_name='word',
            name='count',
        ),
    ]
