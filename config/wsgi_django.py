import os


if not os.environ.has_key('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

import newrelic.agent
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
from whitenoise.django import DjangoWhiteNoise
from ws4redis.uwsgi_runserver import uWSGIWebsocketServer


newrelic.agent.initialize()


application = get_wsgi_application()
application = Sentry(application)
application = newrelic.agent.WSGIApplicationWrapper(application)

_django_app = DjangoWhiteNoise(application)
_websocket_app = uWSGIWebsocketServer()


def application(environ, start_response):
    if environ.get('PATH_INFO').startswith(settings.WEBSOCKET_URL):
        return _websocket_app(environ, start_response)
    return _django_app(environ, start_response)
