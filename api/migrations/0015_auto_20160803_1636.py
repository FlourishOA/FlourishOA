# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-03 16:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20160803_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='influence',
            name='article_influence',
            field=models.DecimalField(decimal_places=7, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='influence',
            name='est_article_influence',
            field=models.DecimalField(decimal_places=7, max_digits=10, null=True),
        ),
    ]
