from .models import Game, Card, Draft, Seed
# from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import GameSerializer, CardSerializer, DraftSerializer, SeedSerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all().order_by('start_date')
    serializer_class = GameSerializer


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class SeedViewSet(viewsets.ModelViewSet):
    queryset = Seed.objects.all()
    serializer_class = SeedSerializer


class DraftViewSet(viewsets.ModelViewSet):
    queryset = Draft.objects.all()
    serializer_class = DraftSerializer

