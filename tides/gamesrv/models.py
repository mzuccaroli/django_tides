# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from random import shuffle, choice


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
    def games_for_user(self, user):
        """Return a queryset of games that this user participates in"""
        return super(GamesManager, self).get_queryset().filter(
            Q(first_player_id=user.id) | Q(second_player_id=user.id))

    def new_game(self, invitation):
        game = Game(
            player_1=invitation.to_user,
            player_2=invitation.from_user,
            current_player=choice([invitation.to_user, invitation.from_user])
        )
        game.save()
        cards = Card.objects.all()
        order = [i for i in range(Card.objects.count())]
        shuffle(order)
        for index, card in enumerate(cards):
            draft = Draft(
                game=game,
                card=card,
                draft_order=order[index]
            )
            draft.save()
        return game


class Game(models.Model):
    player_1 = models.ForeignKey(User, related_name="game_palyer_one", blank=True)
    player_2 = models.ForeignKey(User, related_name="game_palyer_two", blank=True)
    current_player = models.ForeignKey(User, related_name="games_to_move", blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    last_turn_date = models.DateTimeField(auto_now=True)
    finished = models.BooleanField(default=False)
    turn_number = models.IntegerField(default=1)
    deck = models.ManyToManyField(Card, through='Draft', related_name='deck')
    deck_index = models.IntegerField(default=0)
    players_hand = models.ManyToManyField(Card, through='Hand', related_name='players_hand')

    objects = GamesManager()

    def drafted_deck(self):
        return self.deck.order_by('draft__draft_order')

    def get_opponent(self):
        if self.current_player == self.player_1:
            return self.player_2
        else:
            return self.player_1

    def toggle_next_player(self):
        self.current_player == self.get_opponent()

    def prepare_game(self):
        """each player draw 5 cards from deck"""
        for count in range(0, 10):
            self.draw_from_deck()
            self.toggle_next_player()

    def draw_from_deck(self):
        """current player draw a card from deck"""
        hand = Hand(
            game=self,
            card=self.deck[self.deck_index],
            player=self.current_player,
        )
        hand.save()
        self.deck_index += 1

    def get_my_hand(self):
        return self.get_player_hand(self.current_player)

    def get_my_table(self):
        return self.get_player_table(self.current_player)

    def get_opponent_table(self):
        return self.get_player_table(self.get_opponent())

    def redraw_table(self):
        for hand in self.get_my_table():
            hand.draw_card()
            hand.save()

    def get_player_hand(self, user):
        return Hand.get_queryset().filter(game=self, player=user, status="H")

    def get_player_table(self, user):
        return Hand.get_queryset().filter(Q(game=self, player=user, status="T") | Q(game=self, player=user, status="B"))

    def exchange_deck(self):
        first_player_hand = self.get_player_hand(self.player_1)
        second_player_hand = self.get_player_hand(self.player_2)
        for hand in first_player_hand:
            hand.player = self.player_2
            hand.save()
        for hand in second_player_hand:
            hand.player = self.player_1
            hand.save()

    def save(self, *args, **kwargs):
        if self.turn_number <= 10:
            self.turn_number += 1
        else:
            self.finished = True
        self.toggle_next_player()
        super(Game, self).save(*args, **kwargs)

    def __str__(self):
        return "{0} vs {1}".format(self.player_1, self.player_2)


class Draft(models.Model):
    game = models.ForeignKey(Game)
    card = models.ForeignKey(Card)
    draft_order = models.IntegerField()

    class Meta:
        ordering = ['game', 'draft_order']

    def __str__(self):
        return "{0} {1}".format(self.game, self.draft_order)


CARD_STATUS_CHOICES = (
    ('H', 'Hand'),
    ('T', 'Table'),
    ('B', 'Blocked'),
    ('D', 'Discarded')
)


class Hand(models.Model):
    game = models.ForeignKey(Game)
    card = models.ForeignKey(Card)
    player = models.ForeignKey(User, related_name="player_hand", blank=True)
    status = models.CharField(max_length=1, default='H', choices=CARD_STATUS_CHOICES)

    def draw_card(self):
        self.status = "H"

    def play_card(self):
        self.status = "T"

    def block_card(self):
        self.status = "B"

    def discard_card(self):
        self.status = "D"
