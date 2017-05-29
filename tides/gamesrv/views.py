from .models import Game, Card, Draft, Seed, Hand

from django.views import generic
from rest_framework import viewsets
from .serializers import GameSerializer, CardSerializer, DraftSerializer, SeedSerializer, HandSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# class IndexView(generic.ListView):
#     template_name = 'gamesrv/index.html'
#     context_object_name = 'games_list'
#
#     def get_queryset(self):
#         # return Game.objects.filter(player_1=request.user).order_by('last_turn_date')[:5]
#         return Game.objects.all()


class AllGamesList(generic.ListView):
    template_name = 'gamesrv/game_list.html'
    model = Game
    # def get_queryset(self):
    #     # return Game.objects.filter(player_1=request.user).order_by('last_turn_date')[:5]
    #     return Game.objects.all()


@login_required
def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    # if game.is_users_move(request.user):
    #     return redirect('game_do_move', pk=pk)
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
