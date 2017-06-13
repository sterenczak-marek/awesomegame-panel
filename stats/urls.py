# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from .views import StatsIndexView

urlpatterns = [
    url(r'^$', StatsIndexView.as_view(), name='index'),
]
