from .models import Game, Card, Draft, Seed, Hand, Invitation
# from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, reverse

from django.views import generic
from rest_framework import viewsets
from .serializers import GameSerializer, CardSerializer, DraftSerializer, SeedSerializer, HandSerializer, \
    InvitationSerializer
from .forms import InvitationForm


# class IndexView(generic.ListView):
#     template_name = 'gamesrv/index.html'
#     context_object_name = 'games_list'
#
#     def get_queryset(self):
#         # return Game.objects.filter(player_1=request.user).order_by('last_turn_date')[:5]
#         return Game.objects.all()


@login_required
def new_invitation(request):
    if request.method == 'POST':
        invitation = Invitation(from_user=request.user)
        form = InvitationForm(data=request.POST, instance=invitation)
        if form.is_valid():
            form.save()
            return redirect('allgames')
    else:
        form = InvitationForm()
    return render(request, "gamesrv/new_invitation.html", {'form': form})


@login_required
def accept_invitation(request, pk):
    invitation = get_object_or_404(Invitation, pk=pk)
    if not request.user == invitation.to_user:
        raise PermissionDenied
    if request.method == 'POST':
        if "accept" in request.POST:
            game = Game.objects.new_game(invitation)
            game.save()
            invitation.delete()
            return redirect(game)
        else:
            invitation.delete()
            return redirect('user_home')
    else:
        return render(request, "gamesrv/accept_invitation.html", {'invitation': invitation})


class AllGamesList(generic.ListView):
    template_name = 'gamesrv/game_list.html'
    model = Game
    # def get_queryset(self):
    #     # return Game.objects.filter(player_1=request.user).order_by('last_turn_date')[:5]
    #     return Game.objects.all()


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


class InvitationViewSet(viewsets.ModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
