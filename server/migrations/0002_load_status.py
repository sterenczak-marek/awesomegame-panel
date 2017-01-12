from __future__ import unicode_literals

from django.core.management import call_command
from django.db import migrations


def load_fixture(apps, schema_editor):
    call_command('loaddata', 'game_server_status', app_label='server')


class Migration(migrations.Migration):
    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]
