# coding=utf-8

from django.db import models

from awesome_rooms.models import AbstractRoom
from awesome_users.models import GameUser


class Room(AbstractRoom):
    NEW = 0
    IN_PROGRESS = 1

    STATUSES = [
        (NEW, 'Dostępny'),
        (IN_PROGRESS, 'Rozgrywka w trakcie'),
    ]

    game_server = models.ForeignKey('server.GameServer', related_name='rooms', null=True)

    status = models.PositiveIntegerField(default=NEW, choices=STATUSES)

    class Meta:
        db_table = 'rooms'


class PanelUser(GameUser):
    room = models.ForeignKey(Room, null=True, on_delete=models.SET_NULL, related_name='users')

    total_games = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)

    @property
    def looses(self):
        return self.total_games - self.wins
