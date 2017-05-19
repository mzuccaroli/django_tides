from .models import Game, Card, Draft, Seed, Hand, Invitation
# from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from django.views import generic
from rest_framework import viewsets
from .serializers import GameSerializer, CardSerializer, DraftSerializer, SeedSerializer, HandSerializer, \
    InvitationSerializer
from .forms import InvitationForm


# @login_required
class IndexView(generic.ListView):
    template_name = 'tides/index.html'
    context_object_name = 'games_list'

    def get_queryset(self):
        # return Game.objects.filter(player_1=request.user).order_by('last_turn_date')[:5]
        return Game.objects.all()


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
    return render(request, "tides/new_invitation.html", {'form': form})


class AllGamesList(generic.ListView):
    template_name = 'tides/game_list.html'
    model = Game


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
