# -*- coding: utf-8 -*-
'''
Local settings

- Run in Debug mode
- Use console backend for emails
- Add Django Debug Toolbar
- Add django-extensions as app
'''
import os

from .common import *  # noqa

SECRET_KEY = env('DJANGO_SECRET_KEY', default='cTA6ij=RsO7rE^EWHAaYnVVs~,5Qi1aoQZohm4<U6::C]gI5o.')


# TODO: nadpisanie zbedne

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': project_root('AwesomeGameWebPanel.db'),
    }
}

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env("DJANGO_SECRET_KEY", default='n*#ij6(ux!w1l&#nr*8a)-r^evjyz+*s#4%s)obe)h5e99rm!@')

# Mail settings
# ------------------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = project_root('poczta')

# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

BROKER_URL = env('CLOUDAMQP_URL', default='redis://localhost:6379')
CELERY_RESULT_BACKEND = env('CLOUDAMQP_URL', default='redis://localhost:6379')

# SALT_PATH = os.path.join(BASE_DIR, '..', 'salt')

# django-debug-toolbar
# ------------------------------------------------------------------------------
# MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
# INSTALLED_APPS += ('debug_toolbar', )

INTERNAL_IPS = ('127.0.0.1', '10.0.2.2',)

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
