# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-16 15:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamesrv', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='deck',
            field=models.ManyToManyField(related_name='deck', to='gamesrv.Card'),
        ),
    ]
