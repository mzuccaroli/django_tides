from .models import Invitation
from rest_framework import serializers


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ('from_user', 'to_user', 'message', 'timestamp')
