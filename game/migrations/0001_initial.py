# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-30 22:04
from __future__ import unicode_literals

from django.conf import settings
from django.core.management import call_command
from django.db import migrations


def change_site_domain_name(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    Site.objects.update_or_create(
        id=settings.SITE_ID,
        defaults={
            'domain': 'awesomegame.sterenczak.me',
            'name': 'AwesomeGame'
        }
    )

    call_command('loaddata', 'initial_users')

def do_nothing(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique')
    ]

    operations = [
        migrations.RunPython(change_site_domain_name, reverse_code=do_nothing)
    ]
