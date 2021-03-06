# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-05 02:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dictionary', '0004_auto_20170408_2023'),
    ]

    operations = [
        migrations.CreateModel(
            name='Count',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('count_type', models.CharField(choices=[('w', 'word'), ('c', 'character')], default='m', max_length=2)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionary.Entry')),
            ],
        ),
    ]
