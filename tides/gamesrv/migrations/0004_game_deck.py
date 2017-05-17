# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-16 15:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamesrv', '0003_remove_game_deck'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='deck',
            field=models.ManyToManyField(related_name='deck', through='gamesrv.Draft', to='gamesrv.Card'),
        ),
    ]