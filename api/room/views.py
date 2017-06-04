# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import requests
import time

from datadog import initialize, api

from awesome_rooms.models import Room
from awesome_users.serializers import UserSerializer
from django.conf import settings
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

from game.models import RoomInProgress
from server.models import GameServer
from .serializers import RoomSerializer


@receiver(user_logged_out)
def remove_guest(sender, user, request, **kwargs):
    if user.is_guest:
        user.delete()


#
# class GuestRestView(GenericAPIView):
#     serializer_class = LoginGuestSerializer
#     permission_classes = (AllowAny,)
#
#     def post(self, request, *args, **kwargs):
#         user = GameUser.create_guest()
#         user.backend = 'django.contrib.auth.backends.ModelBackend'
#         login(self.request, user)
#
#         return Response("OK", status=status.HTTP_200_OK)


def _get_available_server():
    options = {
        'api_key': settings.DD_API_KEY,
        'app_key': settings.DD_APP_KEY,
    }

    initialize(**options)

    now = int(time.time())
    query = 'system.cpu.user{server:game}by{host}'

    data = api.Metric.query(start=now - 60, end=now, query=query)

    # TODO: dorobić analize i wybor serwera

    server = GameServer.objects.filter(status_id=1).first()

    if server.auth_token is None:
        return None

    return server


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'slug'

    permission_classes = (IsAuthenticated,)

    @detail_route(methods=['get'])
    def users(self, request, **kwargs):
        room = self.get_object()

        serializer = UserSerializer(data=room.users, many=True)
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

    def _start_game(self, room):

        server = _get_available_server()

        if server is None:
            return Response(status=400, data="{'error': 'Brak dostępnego serwera!'}")

        serialized_data = self.get_serializer(instance=room).data

        del serialized_data['slug']
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

            RoomInProgress.objects.create(room=room, game_server=server)

            response_data = response.json()

            for user in response_data.get('users'):
                response = {
                    'type': "PLAY",
                    'url': server_without_leading_slash + "/%s/" % user.get('token'),
                }
                msg = RedisMessage(json.dumps(response))
                RedisPublisher(facility='room_detail', users=[user.get('username')]).publish_message(msg)

            room.status = 1
            room.save()

            return Response(status=302, data=response)

        else:
            return Response(status=400, data=response.json())
