# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-07 11:41
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mediathek', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Angebot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preis', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
            options={
                'verbose_name_plural': 'Angebote',
                'verbose_name': 'Angebot',
            },
        ),
        migrations.CreateModel(
            name='Auftrag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('version', models.PositiveIntegerField(blank=True)),
                ('datum', models.DateField(default=datetime.datetime.today, verbose_name='Auftrags-Datum')),
                ('status', models.IntegerField(choices=[(0, 'erstellt'), (1, 'bearbeitet'), (2, 'abgeschlossen')], default=0)),
            ],
            options={
                'verbose_name_plural': 'Aufträge',
                'verbose_name': 'Auftrag',
                'ordering': ('-datum', '-created_date'),
            },
        ),
        migrations.CreateModel(
            name='Sammelbestellung',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bezeichnung', models.CharField(max_length=30)),
                ('start', models.DateTimeField()),
                ('ende', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': 'Sammelbestellungen',
                'verbose_name': 'Sammelbestellung',
            },
        ),
        migrations.CreateModel(
            name='Ware',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bezeichnung', models.CharField(max_length=30)),
                ('marke', models.CharField(blank=True, max_length=30, null=True)),
                ('variation', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'verbose_name_plural': 'Waren',
                'verbose_name': 'Ware',
            },
        ),
        migrations.RemoveField(
            model_name='kunde',
            name='kunden_email',
        ),
        migrations.RemoveField(
            model_name='kunde',
            name='kunden_id',
        ),
        migrations.RemoveField(
            model_name='kunde',
            name='kunden_name',
        ),
        migrations.RemoveField(
            model_name='kunde',
            name='kunden_vorname',
        ),
        migrations.AlterField(
            model_name='kunde',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Bestellung',
            fields=[
                ('auftrag_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mediathek.Auftrag')),
                ('anzahl', models.IntegerField(default=1)),
            ],
            options={
                'verbose_name_plural': 'Sammelbestellungen(Aufträge)',
                'verbose_name': 'Sammelbestellung(Auftrag)',
            },
            bases=('mediathek.auftrag',),
        ),
        migrations.AddField(
            model_name='auftrag',
            name='created_by',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='auftrag',
            name='modified_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='angebot',
            name='sammelbestellung',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mediathek.Sammelbestellung'),
        ),
        migrations.AddField(
            model_name='angebot',
            name='ware',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mediathek.Ware'),
        ),
        migrations.AddField(
            model_name='bestellung',
            name='angebot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mediathek.Angebot'),
        ),
    ]