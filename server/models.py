# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from autoslug.utils import slugify
from awesome_users.models import GameUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy
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
    name = models.CharField("Nazwa", max_length=256, default='', unique=True)
    slug = models.SlugField()

    url = models.URLField("Adres URL", unique=True)
    auth_token = models.CharField("Token uwierzytelniający", max_length=256)
    datadog_hostname = models.CharField("Nazwa hosta w datadog", max_length=256)

    status = models.ForeignKey(GameServerStatus, default=1)

    panel_user = models.ForeignKey(GameUser, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)

        return super(GameServer, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('server:detail', args=[self.pk])

    @property
    def can_delete(self):
        return self.status.pk in [1, 9]


@receiver(post_save, sender=GameServer)
def after_adding_game_server(sender, instance, created, **kwargs):
    if created:
        user = GameUser.objects.create(username="system: %s" % instance.name, password="!")
        instance.panel_user = user
        instance.save()

        Token.objects.create(user=user)
