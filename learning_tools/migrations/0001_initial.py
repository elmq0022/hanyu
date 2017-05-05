# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-29 15:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dictionary', '0004_auto_20170408_2023'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('count_type', models.CharField(choices=[('UN', 'unlearned'), ('AC', 'acquiring'), ('LN', 'learned')], default='UN', max_length=2)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionary.Entry')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='word',
            unique_together=set([('entry', 'user')]),
        ),
    ]