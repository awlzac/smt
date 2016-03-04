# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-04 02:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addrmap', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='lat',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='lng',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]