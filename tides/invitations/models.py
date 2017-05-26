# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Invitation(models.Model):
    from_user = models.ForeignKey(User, related_name="invitations_sent")
    to_user = models.ForeignKey(User, related_name="invitations_received", verbose_name="User to invite",
                                help_text="Please select the user you want to play a game with")
    message = models.CharField("Optional Message", max_length=300, blank=True,
                               help_text="Adding a friendly message is never a bad idea!")
    timestamp = models.DateTimeField(auto_now_add=True)
