from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

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


class ServerDeleteView(AdminMixin, DeleteView):
    model = GameServer
    success_url = reverse_lazy('server:list')


class ServerDetailView(AdminMixin, DetailView):
    model = GameServer
