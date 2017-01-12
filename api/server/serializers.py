# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from server.models import GameServer


class GameServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameServer
        fields = ['name', 'url']

