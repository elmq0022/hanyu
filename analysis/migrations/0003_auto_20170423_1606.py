# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-23 21:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0004_auto_20170408_2023'),
        ('analysis', '0002_auto_20170422_2130'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultiCounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionary.Entry')),
            ],
        ),
        migrations.CreateModel(
            name='SingleCounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionary.Entry')),
            ],
        ),
        migrations.RemoveField(
            model_name='frequency',
            name='entry',
        ),
        migrations.DeleteModel(
            name='Frequency',
        ),
    ]
