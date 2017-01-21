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
    fields = ['name', 'url']
    success_url = reverse_lazy('server:list')


class ServerDetailView(AdminMixin, DetailView):
    model = GameServer

    def get_context_data(self, **kwargs):
        context = super(ServerDetailView, self).get_context_data(**kwargs)

        salt_root = environ.Path(settings.SALT_PATH)
        public_key_path = salt_root('_pki/ssh/salt-ssh.rsa.pub')

        with open(public_key_path) as public_key_file:
            ssh_key = public_key_file.read()

        context.update({
            'public_ssh_key': ssh_key
        })
        return context
