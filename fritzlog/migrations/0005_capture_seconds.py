# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 03:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fritzlog', '0004_capture'),
    ]

    operations = [
        migrations.AddField(
            model_name='capture',
            name='seconds',
            field=models.IntegerField(default=0, verbose_name='length in seconds'),
            preserve_default=False,
        ),
    ]
