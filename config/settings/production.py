from .common import *  # noqa

DEBUG = True

STATIC_ROOT = project_root('staticfiles')
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

DATABASES = {
    'default': env.db(), # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
    'extra': env.db('SQLITE_URL', default='sqlite:////tmp/my-tmp-sqlite.db')
}

ALLOWED_HOSTS = [
    'awesomegame-panel.herokuapp.com',
]