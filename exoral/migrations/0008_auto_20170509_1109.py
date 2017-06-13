# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-09 09:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    def physikum(apps, schema_editor):
        Testat = apps.get_model("exoral", "Testat")
        physikum = Testat(bezeichnung = "Physikum")
        physikum.save()

        Frage = apps.get_model("exoral", "Frage")
        for frag in Frage.objects.filter(testat__bezeichnung__startswith = "PHYSIKUM"):
            frag.testat = physikum
            frag.save()

    dependencies = [
        ('exoral', '0007_auto_20170509_1058'),
    ]

    operations = [
        migrations.RunPython(physikum),
    ]
