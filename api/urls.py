# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import routers

from api.room.views import RoomViewSet
from api.server.views import GameServerViewSet

router = routers.DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'servers', GameServerViewSet)

urlpatterns = router.urls

