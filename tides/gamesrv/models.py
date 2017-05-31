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
        # game.prepare_game()
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

    def get_opponent(self, player):
        if player == self.player_1:
            return self.player_2
        else:
            return self.player_1

    def toggle_next_player(self):
        self.current_player = self.get_opponent(self.current_player)

    def prepare_game(self):
        self.shuffle_deck()
        """each player draw 5 cards from deck"""
        for count in range(0, 10):
            self.draw_from_deck()
            self.toggle_next_player()
        self.save()

    def shuffle_deck(self):
        cards = Card.objects.all()
        order = [i for i in range(Card.objects.count())]
        shuffle(order)
        for index, card in enumerate(cards):
            draft = Draft(
                game=self,
                card=card,
                draft_order=order[index]
            )
            draft.save()

    def draw_from_deck(self):
        """current player draw a card from deck"""
        card = self.deck.get(draft__draft_order=self.deck_index)
        hand = Hand(
            game=self,
            card=card,
            player=self.current_player,
        )
        hand.save()
        self.deck_index += 1
        Draft.objects.get(card=card, game=self).delete()

    def redraw_table(self):
        for hand in self.get_my_table():
            hand.draw_card()
            hand.save()

    def player_1_hand(self):
        return self.players_hand.filter(hand__game=self, hand__player=self.player_1, hand__status="H")

    def player_2_hand(self):
        return self.players_hand.filter(hand__game=self, hand__player=self.player_2, hand__status="H")

    def player_1_table(self):
        return self.players_hand.filter(
            Q(hand__game=self, hand__player=self.player_1, hand__status="T") |
            Q(hand__game=self, hand__player=self.player_1, hand__status="B")
        )

    def player_2_table(self):
        return self.players_hand.filter(
            Q(hand__game=self, hand__player=self.player_2, hand__status="T") |
            Q(hand__game=self, hand__player=self.player_2, hand__status="B")
        )

    def get_player_table(self, user):
        return self.players_hand.filter(
            Q(hand__game=self, hand__player=user, hand__status="T") | Q(hand__game=self, hand__player=user,
                                                                        hand__status="B"))

    def exchange_hands(self):
        for hand in Hand.objects.filter(game=self, status="H"):
            if hand.player == self.player_1:
                hand.player = self.player_2
            else:
                hand.player = self.player_1
            hand.save()

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
