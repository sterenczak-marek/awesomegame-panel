# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DetailView, ListView

from game.models import PanelUser


class StatsIndexView(DetailView):
    model = PanelUser
    template_name = 'stats/detail.html'

    def get_object(self):
        return self.request.user

