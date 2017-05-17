# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Game, Card, Draft, Seed

# Register your models here.

admin.site.register(Game)
admin.site.register(Card)
admin.site.register(Draft)
admin.site.register(Seed)
