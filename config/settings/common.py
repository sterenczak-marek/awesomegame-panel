# -*- coding: utf-8 -*-
"""
Django settings for src project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from __future__ import absolute_import, unicode_literals

import environ

project_root = environ.Path(__file__) - 3  # (/a/b/myfile.py - 3 = /)

env = environ.Env()
environ.Env.read_env(project_root('.env'))


SITE_ROOT = project_root()
SALT_PATH = project_root('salt')

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    # Default Django src:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin
    'django.contrib.admin',
)
THIRD_PARTY_APPS = (
    'crispy_forms',  # Form layouts
    'allauth',  # registration
    'allauth.account',  # registration
    'allauth.socialaccount',  # registration

    'ws4redis',
    'rest_framework',
    'rest_framework.authtoken',

    'djangobower',
)

# Apps specific for this project go here.
LOCAL_APPS = (

    'awesome_rooms',
    'awesome_users',

    'api',
    'game',
    'server',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES = (
    # Make sure djangosecure.middleware.SecurityMiddleware is listed first
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'awesome_staff.middleware.WhodidMiddleware',
    'awesome_staff.middleware.LoginRequiredMiddleware',
)

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    # 'sites': 'contrib.sites.migrations'
}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ("""Marek Stereńczak""", 'ms42091@st.amu.edu.pl'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'pl_PL'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            project_root('templates'),
        ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # Your stuff: custom template context processors go here

                'ws4redis.context_processors.default',
            ],
        },
    },
]

# See: http://django-crispy-forms.readthedocs.org/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    project_root('static'),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    'djangobower.finders.BowerFinder',
)


STATIC_ROOT = project_root('staticfiles')
BOWER_COMPONENTS_ROOT = project_root('vendor')


BOWER_INSTALLED_APPS = (
    "bootstrap#3.3.1",
    "font-awesome#4.2.0",
    "datatables-plugins#1.0.1",
    "datatables-responsive#1.0.3",
    "reset-css",
    "jquery#2.1.3",
    "lodash#3.7.0",
    "gentelella#1.4.0",
    "datatables.net#1.10.11",
    "datatables.net#^1.10.11",
    "datatables.net-bs#^1.10.11",
    "datatables.net-buttons#^1.1.2",
    "datatables.net-buttons-bs#^1.1.2",
    "datatables.net-fixedheader#^3.1.1",
    "datatables.net-fixedheader-bs#^3.1.1",
    "datatables.net-keytable#^2.1.1",
    "datatables.net-responsive#^2.0.2",
    "datatables.net-responsive-bs#^2.0.2",
    "datatables.net-scroller#^1.4.1",
    "datatables.net-scroller-bs#^1.4.1",
    "icheck#^1.0.2"   ,
    "bootstrap-progressbar#^0.9.0",
    "nprogress#^0.2.0",
    "fastclick#^1.0.6",
    "animate.css#3.5.2"
)


# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = project_root('media')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
# WSGI_APPLICATION = 'config.wsgi.application'
WSGI_APPLICATION = 'ws4redis.django_runserver.application'

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # 'allauth.account.auth_backends.AuthenticationBackend',
)

# Some really nice defaults
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
#
# ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
# SOCIALACCOUNT_ADAPTER = 'awesome_users.adapters.SocialAccountAdapter'

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = 'game.PanelUser'

# LOGIN_REDIRECT_URL = 'users:redirect'
# LOGIN_URL = 'account_login'

# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

EMAIL_SUBJECT_PREFIX = '[AwesomeGame]'
DEFAULT_FROM_EMAIL = 'no-reply@awesomegame.sterenczak.me'

# CELERY
BROKER_POOL_LIMIT = 3
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = r'^admin/'

# Your common stuff: Below this line define 3rd party library settings
WEBSOCKET_URL = '/ws/'

WS4REDIS_EXPIRE = 2
WS4REDIS_PREFIX = 'ws'
WS4REDIS_HEARTBEAT = '--heartbeat--'
WS4REDIS_ALLOWED_CHANNELS = 'common.redis'

WS4REDIS_CONNECTION = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 2
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'api.config.DatatablePagination',
    # 'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
}

RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
RECAPTCHA_PRIVATE_KEY = '98dfg6df7g56df6gdfgdfg65JHJH656565GFGFGs'
NOCAPTCHA = True

LOGIN_REDIRECT_URL = '/'
LOGIN_EXEMPT_URLS = [""]
