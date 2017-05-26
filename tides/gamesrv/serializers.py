from .models import Game, Card, Draft, Seed, Hand
from rest_framework import serializers


class SeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seed
        fields = ('id', 'name')


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('id', 'name', 'description', 'image_url', 'seed')


class CardSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('id', 'name')


class GameSerializer(serializers.ModelSerializer):
    deck = CardSummarySerializer(many=True)

    class Meta:
        model = Game
        fields = ('id', 'player_1', 'player_2', 'start_date', 'last_turn_date', 'finished', 'turn_number', 'deck')


class DraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = ('game_id', 'card_id', 'draft_order')


class HandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hand
        fields = ('game', 'player', 'card', 'status')

