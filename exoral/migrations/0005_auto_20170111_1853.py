# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-11 17:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exoral', '0004_auto_20170111_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frage',
            name='datum',
            field=models.DateField(default=datetime.datetime.today),
        ),
    ]