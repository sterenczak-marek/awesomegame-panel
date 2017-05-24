import environ

import numpy
import time

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView

from datadog import initialize, api

from .models import GameServer


class AdminMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super(AdminMixin, self).dispatch(request, *args, **kwargs)

        raise PermissionDenied


class ServerListView(AdminMixin, ListView):
    model = GameServer


class ServerCreateView(AdminMixin, CreateView):
    model = GameServer
    fields = ['name', 'url', 'auth_token']
    success_url = reverse_lazy('server:list')


class ServerDetailView(AdminMixin, DetailView):
    model = GameServer

    def get_context_data(self, *args, **kwargs):
        context = super(ServerDetailView, self).get_context_data(*args, **kwargs)


        options = {
            'api_key': settings.DD_API_KEY,
            'app_key': settings.DD_APP_KEY,
        }

        initialize(**options)

        now = int(time.time())
        query = 'system.cpu.user{server:game}by{host}'
        data = api.Metric.query(start=now - 60, end=now, query=query)

        cpu_list = [item[1] for item in data['series'][0]['pointlist']]
        avg_cpu = numpy.mean(cpu_list)

        query = 'system.mem.used{server:game}by{host}'
        data = api.Metric.query(start=now - 60, end=now, query=query)

        memory_list = [item[1] for item in data['series'][0]['pointlist']]
        avg_ram = numpy.mean(memory_list)

        context.update({
            'stats': {
                'cpu': round(avg_cpu, 2),
                'ram':  int(avg_ram)
            }
        })

        return context
