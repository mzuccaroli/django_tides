from .models import Invitation
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


class InvitationViewSet(viewsets.ModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer