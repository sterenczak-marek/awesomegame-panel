# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

import numpy
from autoslug.utils import slugify
from datadog import initialize, api
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.utils.encoding import python_2_unicode_compatible
from rest_framework.authtoken.models import Token

from game.models import PanelUser


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

    panel_user = models.ForeignKey(PanelUser, null=True, blank=True)

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

    @property
    def stats(self):
        options = {
            'api_key': settings.DD_API_KEY,
            'app_key': settings.DD_APP_KEY,
        }

        initialize(**options)

        now = int(time.time())
        query = 'system.cpu.user{host:%s}' % self.datadog_hostname
        cpu_data = api.Metric.query(start=now - 3600, end=now, query=query)

        query = 'system.mem.used{host:%s}' % self.datadog_hostname
        memory_used = api.Metric.query(start=now - 3600, end=now, query=query)

        query = 'system.mem.total{host:%s}' % self.datadog_hostname
        memory_total = api.Metric.query(start=now - 3600, end=now, query=query)

        cpu, ram = None, None

        if cpu_data['series']:
            cpu_list = [item[1] for item in cpu_data['series'][0]['pointlist']]
            avg_cpu = numpy.mean(cpu_list)
            cpu = round(avg_cpu, 2)

        if memory_used['series']:
            memory_used_list = [item[1] for item in memory_used['series'][0]['pointlist']]
            memory_total_list = [item[1] for item in memory_total['series'][0]['pointlist']]
            avg_ram = numpy.mean(memory_used_list)
            avg_total_ram = numpy.mean(memory_total_list)
            ram = (avg_ram / avg_total_ram) * 100

        return {
            'cpu': cpu,
            'ram': round(ram, 2)
        }


@receiver(post_save, sender=GameServer)
def after_adding_game_server(sender, instance, created, **kwargs):
    if created:
        user = PanelUser.objects.create(username="system: %s" % instance.name, password="!")
        instance.panel_user = user
        instance.save()

        Token.objects.create(user=user)
