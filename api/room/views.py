# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import requests
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

from api.serializers import PanelUserSerializer
from game.models import Room
from server.models import GameServer
from .serializers import RoomSerializer

User = get_user_model()


def _get_available_server():
    game_server_stats = {}

    for game_server in GameServer.objects.exclude(status=9):
        game_server_stats[game_server] = game_server.stats['ram']

    return min(game_server_stats, key=game_server_stats.get)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'slug'

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    @detail_route(methods=['get'])
    def users(self, request, **kwargs):
        room = self.get_object()

        serializer = PanelUserSerializer(data=room.users, many=True)
        serializer.is_valid()

        return Response(serializer.data)

    @detail_route(methods=['get'])
    def allowed_actions(self, request, **kwargs):
        room = self.get_object()

        if room.status == 0:
            return Response({
                'join': request.user.room is None and room.users.count() < room.max_players,
                'leave': request.user.room == room,
                'ready': request.user.room == room and not request.user.ready_to_play,
                'unready': request.user.room == room and request.user.ready_to_play,
            })
        else:
            return Response({})

    @detail_route(methods=['post'])
    def join(self, request, **kwargs):
        room = self.get_object()

        if request.user.is_admin:
            raise ValidationError('User jest już adminem')

        request.user.room = room
        request.user.ready_to_play = False
        request.user.save()

        response = self.users(request, **kwargs)

        msg = RedisMessage(json.dumps(response.data))
        RedisPublisher(facility='room_detail', groups=[str(room)]).publish_message(msg)

        return response

    @detail_route(methods=['post'])
    def leave(self, request, **kwargs):
        room = self.get_object()

        if request.user.room != room:
            raise ValidationError('Nie możesz opuścić pokoju w którym Cie nie ma')

        request.user.room = None
        request.user.save(update_fields=['room'])

        if request.user.is_admin:

            request.user.is_admin = False
            request.user.save(update_fields=['is_admin'])

            if room.users.exists():
                new_admin = room.users.first()
                new_admin.is_admin = True
                new_admin.save(update_fields=['is_admin'])

        if not room.users.exists():
            # TODO: self.destroy(request, **kwargs)
            pass

        response = self.users(request, **kwargs)

        msg = RedisMessage(json.dumps(response.data))
        RedisPublisher(facility='room_detail', groups=[str(room)]).publish_message(msg)

        return response

    @detail_route(methods=['post'])
    def unready(self, request, **kwargs):
        request.user.ready_to_play = False
        request.user.save(update_fields=['ready_to_play'])

        room = self.get_object()

        response = self.users(request, **kwargs)
        msg = RedisMessage(json.dumps(response.data))
        RedisPublisher(facility='room_detail', groups=[str(room)]).publish_message(msg)

        return response

    @detail_route(methods=['post'])
    def ready(self, request, **kwargs):
        request.user.ready_to_play = True
        request.user.save(update_fields=['ready_to_play'])

        room = self.get_object()
        game_ready = all([user.ready_to_play for user in room.users.all()])

        if game_ready:
            return self._start_game(room)

        else:
            response = self.users(request, **kwargs)
            msg = RedisMessage(json.dumps(response.data))
            RedisPublisher(facility='room_detail', groups=[str(room)]).publish_message(msg)

            return response

    @detail_route(methods=['post'])
    def finished(self, request, **kwargs):
        room = self.get_object()

        received_data = request.data

        winner = User.objects.get(id=received_data['winner']['panel_user_id'])

        winner.wins += 1
        winner.save()

        room.status = 0
        room.save()

        for user in room.users.all():
            user.ready_to_play = False
            user.save()

        ret_data = {
            'url_path': reverse('room:detail', args=[room.slug])
        }

        return Response(status=200, data=json.dumps(ret_data))

    def _start_game(self, room):

        server = _get_available_server()
        server_user_token, _ = Token.objects.get_or_create(user=server.panel_user)

        if server is None:
            return Response(status=400, data="{'error': 'Brak dostępnego serwera!'}")

        serialized_data = self.get_serializer(instance=room).data

        serialized_data.update({
            'auth_token': str(server_user_token),
            'panel_room_id': room.pk,
            'panel_room_slug': room.slug
        })

        data = json.dumps(serialized_data)
        server_without_leading_slash = server.url.rstrip('/')

        response = requests.post(
            server_without_leading_slash + "/api/rooms/create/",
            data=data,
            headers={
                "Authorization": "Token %s" % server.auth_token,
                "Content-Type": "application/json",
            })

        if response.status_code == 201:

            room.server = server
            room.save()

            for user in room.users.all():
                user.total_games += 1
                user.save()

            response_data = response.json()

            for user_data in response_data.get('users'):
                response = {
                    'type': "PLAY",
                    'url': server_without_leading_slash + "/%s/" % user_data.get('token'),
                }
                msg = RedisMessage(json.dumps(response))
                user = User.objects.get(id=user_data['panel_user_id'])
                RedisPublisher(facility='room_detail', users=[user.username]).publish_message(msg)

            room.status = 1
            room.save()

            return Response(status=200, data=response)

        else:
            return Response(status=400, data=response.content)
