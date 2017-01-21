# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import environ
import yaml
from autoslug.utils import slugify
from awesome_users.models import GameUser
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from rest_framework.authtoken.models import Token

@python_2_unicode_compatible
class GameServerStatus(models.Model):
    status = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class GameServer(models.Model):
    name = models.CharField(max_length=256, default='', unique=True)
    slug = models.SlugField()

    url = models.URLField(unique=True)
    auth_token = models.CharField(max_length=256, blank=True)

    status = models.ForeignKey(GameServerStatus, default=10)

    panel_user = models.ForeignKey(GameUser, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if not self.pk:
            self.slug = slugify(self.name)

            name = 'game-server-%s' % self.slug

            roster_config = {
                name: {
                    'user': 'ubuntu',
                    'host': self.url.split('//')[1],
                    'sudo': True
                }
            }
            salt_roster_path = environ.Path(settings.SALT_PATH)('config/roster')
            with open(salt_roster_path, 'w+') as salt_roster_file:
                yaml.safe_dump(roster_config, salt_roster_file, indent=4, default_flow_style=False)


        return super(GameServer, self).save(*args, **kwargs)


@receiver(post_save, sender=GameServer)
def after_adding_game_server(sender, instance, created, **kwargs):
    if created:
        user = GameUser.objects.create(username="system: %s" % instance.name, password="!")
        instance.panel_user = user
        instance.save()

        Token.objects.create(user=user)
