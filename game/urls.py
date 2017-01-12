# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from .views import RoomListView, RoomDetailView, RoomCreateView

urlpatterns = [
    url(r'^$', RoomListView.as_view(), name='list'),
    url(r'^create/$', RoomCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', RoomDetailView.as_view(), name='detail'),
]
