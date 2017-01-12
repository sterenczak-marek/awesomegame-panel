# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated

from server.models import GameServer
from common.celery import app as celery_app

from .serializers import GameServerSerializer


class GameServerViewSet(viewsets.ModelViewSet):
    queryset = GameServer.objects.all()
    serializer_class = GameServerSerializer

    permission_classes = (IsAuthenticated,)

    @detail_route(methods=['post'])
    def run(self, request, **kwargs):
        server = self.get_object()

        server.status_id = 6
        server.save(update_fields=['status_id'])
        host = urlparse(server.url).hostname
        celery_app.send_task('gameserver.create', args=[server.pk, host])

        return self.retrieve(request, **kwargs)

