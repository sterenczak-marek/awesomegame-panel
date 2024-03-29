# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-08 22:31
from __future__ import unicode_literals

from django.db import migrations


def initial_users(apps, schema_editor):
    _PanelUser = apps.get_model('game', 'PanelUser')
    _PanelUser.objects.bulk_create([
        _PanelUser(
            password="pbkdf2_sha256$30000$wRFGgClK5yq5$5Dh9HX74DqtIyLD522uK7U8mdYG2xvA/r1BxF11SHzE=",
            username="admin",
            email="ms42091@st.amu.edu.pl",
            is_superuser=True,
            is_staff=True
        )
    ])


def delete_initial_users(apps, schema_editor):
    _PanelUser = apps.get_model('game', 'PanelUser')
    _PanelUser.objects.filter(username="admin").delete()


class Migration(migrations.Migration):
    dependencies = [
        ('game', '0002_site_name'),
    ]

    operations = [
        migrations.RunPython(initial_users, reverse_code=delete_initial_users)
    ]
