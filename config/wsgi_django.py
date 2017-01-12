import os
import newrelic.agent

from django.core.wsgi import get_wsgi_application

newrelic.agent.initialize()

os.environ.update(DJANGO_SETTINGS_MODULE="config.settings.production")

application = get_wsgi_application()
application = newrelic.agent.WSGIApplicationWrapper(application)
