# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-16 15:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamesrv', '0002_game_deck'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='deck',
        ),
    ]
