# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-16 02:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.TextField(editable=False),
        ),
    ]
