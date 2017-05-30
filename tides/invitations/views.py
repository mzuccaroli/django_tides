from .models import Invitation
from django.views import generic
from gamesrv.models import Game
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .forms import InvitationForm
from .serializers import InvitationSerializer


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
    return render(request, "invitations/new_invitation.html", {'form': form})


@login_required
def accept_invitation(request, pk):
    invitation = get_object_or_404(Invitation, pk=pk)
    if not request.user == invitation.to_user:
        raise PermissionDenied
    if request.method == 'POST':
        if "accept" in request.POST:
            game = Game.objects.new_game(invitation)
            # invitation.delete()
            return redirect('game_detail', pk=game.pk)
        else:
            invitation.delete()
            return redirect('user_home')
    else:
        return render(request, "invitations/accept_invitation.html", {'invitation': invitation})


class AllInvitationsList(generic.ListView):
    template_name = 'invitations/invitation_list.html'
    model = Invitation
    # def get_queryset(self):
    #     # return Game.objects.filter(player_1=request.user).order_by('last_turn_date')[:5]
    #     return Game.objects.all()


class InvitationViewSet(viewsets.ModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
