# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

from game.models import Room


class RoomListView(ListView):
    model = Room
    template_name = 'room/list.html'


class RoomDetailView(DetailView):
    model = Room
    template_name = 'room/detail.html'

    def get(self, request, *args, **kwargs):
        response = super(RoomDetailView, self).get(request, *args, **kwargs)
        request.session['ws4redis:memberof'] = [str(self.object)]
        return response


class RoomCreateView(CreateView):
    model = Room
    fields = ['name', 'max_players']
    template_name = 'room/create.html'

    def get_success_url(self, *args):
        return reverse('room:detail', args=[self.object.slug])

    def form_valid(self, form):
        ret = super(RoomCreateView, self).form_valid(form)

        self.request.user.room = self.object
        self.request.user.is_admin = True
        self.request.user.ready_to_play = False
        self.request.user.save()

        msg = RedisMessage('Room %s created' % self.object)
        RedisPublisher(facility='room_list', broadcast=True).publish_message(msg)

        return ret
