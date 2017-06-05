from rest_framework import serializers

from awesome_users.serializers import UserSerializer
from game.models import PanelUser


class PanelUserSerializer(UserSerializer):
    panel_user_id = serializers.IntegerField(source='id')

    class Meta:
        model = PanelUser
        fields = ['username', 'is_admin', 'ready_to_play', 'panel_user_id']
