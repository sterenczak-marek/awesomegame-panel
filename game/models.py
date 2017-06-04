from awesome_rooms.models import Room
from django.db import models


class RoomInProgress(models.Model):
    room = models.OneToOneField(Room)
    game_server = models.ForeignKey('server.GameServer', related_name='rooms')

    class Meta:
        db_table = 'room_game_server'
