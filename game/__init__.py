# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from common.celery import app as celery_app  # noqa
