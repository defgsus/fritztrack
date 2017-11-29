# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 02:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fritzlog', '0002_connecteddevice'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='connecteddevice',
            options={'verbose_name': 'Connected Device', 'verbose_name_plural': 'Connected Devices'},
        ),
        migrations.AddField(
            model_name='connecteddevice',
            name='ip',
            field=models.CharField(default='', max_length=20, verbose_name='IP'),
            preserve_default=False,
        ),
    ]
