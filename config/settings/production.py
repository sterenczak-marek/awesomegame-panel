from .common import *  # noqa

DEBUG = True

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

DATABASES = {
    'default': env.db(), # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
    'extra': env.db('SQLITE_URL', default='sqlite:////tmp/my-tmp-sqlite.db')
}

ALLOWED_HOSTS = [
    'awesomegame-panel.herokuapp.com',
]

# Mail settings
# ------------------------------------------------------------------------------
EMAIL_BACKEND = 'django_mailgun.MailgunBackend'

MAILGUN_ACCESS_KEY = env('MAILGUN_ACCESS_KEY')
MAILGUN_SERVER_NAME = env('MAILGUN_SERVER_NAME')

BROKER_URL = env('CLOUDAMQP_URL')
CELERY_RESULT_BACKEND = env('CLOUDAMQP_URL')
