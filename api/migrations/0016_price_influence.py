# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-09 21:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20160803_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='influence',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Influence'),
        ),
    ]
