# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-26 17:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poster', '0002_auto_20171026_0200'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='rejected_at',
            field=models.DateTimeField(null=True),
        ),
    ]
