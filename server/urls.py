# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from .views import ServerListView, ServerCreateView, ServerDetailView, ServerEditView

urlpatterns = [
   url(r'^$', ServerListView.as_view(), name='list'),
   url(r'^create/$', ServerCreateView.as_view(), name='create'),
   url(r'^(?P<pk>[0-9]+)/$', ServerDetailView.as_view(), name='detail'),
   url(r'^(?P<pk>[0-9]+)/edit$', ServerEditView.as_view(), name='edit'),
]
