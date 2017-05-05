# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-05 01:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_tools', '0004_auto_20170504_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordlearningstatus',
            name='learning_status',
            field=models.CharField(choices=[('UN', 'unlearned'), ('AC', 'acquiring'), ('LN', 'learned')], default='UN', max_length=2),
        ),
    ]
