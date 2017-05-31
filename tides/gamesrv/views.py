from .models import Game, Card, Draft, Seed, Hand

from django.views import generic
from rest_framework import viewsets
from .serializers import GameSerializer, CardSerializer, DraftSerializer, SeedSerializer, HandSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404


class AllGamesList(generic.ListView):
    template_name = 'gamesrv/game_list.html'
    model = Game

    def get_queryset(self):
        return Game.objects.filter(player_1=self.request.user)


@login_required
def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        if "prepare" in request.POST:
            game.prepare_game()
            return redirect('game_detail', pk=game.pk)
        elif "switch" in request.POST:
            game.exchange_hands()
    return render(request, "gamesrv/game_detail.html", {'game': game})


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


class HandViewSet(viewsets.ModelViewSet):
    queryset = Hand.objects.all()
    serializer_class = HandSerializer
