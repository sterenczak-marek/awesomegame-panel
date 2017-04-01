import environ
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView

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
