import time

import numpy
from datadog import api, initialize
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

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
    fields = ['name', 'url', 'auth_token', 'datadog_hostname']
    success_url = reverse_lazy('server:list')


class ServerEditView(AdminMixin, UpdateView):
    model = GameServer
    fields = ['url', 'auth_token', 'datadog_hostname', 'status']


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
        query = 'system.cpu.user{host:%s}' % self.object.datadog_hostname
        cpu_data = api.Metric.query(start=now - 3600, end=now, query=query)

        query = 'system.mem.used{host:%s}' % self.object.datadog_hostname
        mem_data = api.Metric.query(start=now - 3600, end=now, query=query)

        cpu, ram = None, None

        if cpu_data['series']:
            cpu_list = [item[1] for item in cpu_data['series'][0]['pointlist']]
            avg_cpu = numpy.mean(cpu_list)
            cpu = round(avg_cpu, 2)

        if mem_data['series']:
            memory_list = [item[1] for item in mem_data['series'][0]['pointlist']]
            avg_ram = numpy.mean(memory_list)
            ram = int(avg_ram)

        context.update({
            'stats': {
                'cpu': cpu,
                'ram': ram
            }
        })

        return context
