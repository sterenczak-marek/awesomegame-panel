web: gunicorn config.wsgi --log-file -

worker: celery worker -A common.celery -l info
