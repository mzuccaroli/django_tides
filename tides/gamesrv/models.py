# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from random import shuffle


class Seed(models.Model):
    name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Card(models.Model):
    name = models.CharField(max_length=200)
    seed = models.ForeignKey(Seed, related_name="seed_of_the_card")
    description = models.CharField(max_length=200, blank=True)
    image_url = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class GamesManager(models.Manager):

    def new_game(user):
        cards = Card.objects.all()
        order = [i for i in range(Card.objects.count())]
        shuffle(order)

        game = Game(first_player=user)
        game.save()

        for index, card in enumerate(cards):
            draft = Draft(
                game=game.id,
                card=card.id,
                draft_order=order[index]
            )
            draft.save()
        return game


class Game(models.Model):
    player_1 = models.ForeignKey(User, related_name="game_palyer_one", blank=True)
    player_2 = models.ForeignKey(User, related_name="game_palyer_two", blank=True)
    next_to_move = models.ForeignKey(User, related_name="games_to_move", blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    last_turn_date = models.DateTimeField(auto_now=True)
    finished = models.BooleanField()
    turn_number = models.IntegerField(default=1)
    deck = models.ManyToManyField(Card, through='Draft', related_name='deck')

    objects = GamesManager()

    # def shuffle_deck(self):
    #     shuffle(self.deck)

    def __str__(self):
        return self.player_1 + '_vs_' + self.player_2

    def __str__(self):
        return "{0} vs {1}".format(self.player_1, self.player_2)

    def save(self, *args, **kwargs):
        # if self.pk is None:
        #     cards = Card.objects.all()
        #     shuffle(cards)
        #     for card in cards:
        #         self.deck.add(card)

        if self.turn_number <= 10:
            self.turn_number += 1
        else:
            self.finished = True
        super(Game, self).save(*args, **kwargs)


class Draft(models.Model):
    game = models.ForeignKey(Game)
    card = models.ForeignKey(Card)
    draft_order = models.IntegerField()
