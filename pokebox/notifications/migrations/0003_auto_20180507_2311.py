# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-07 23:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20180507_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegram',
            name='name',
            field=models.CharField(default='', editable=False, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='telegram',
            name='token',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
