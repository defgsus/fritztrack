# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from picklefield import PickledObjectField


class MongoDbConnection(models.Model):
    class Meta:
        verbose_name = _("MongoDB Connection")
        verbose_name_plural = _("MongoDB Connections")

    date = models.DateTimeField(verbose_name=_("date"))
    host = models.CharField(verbose_name=_("hostname"), max_length=256)
    port = models.SmallIntegerField(verbose_name=_("port"))
    is_error = models.BooleanField(verbose_name=_("is error"), default=False)
    data = PickledObjectField(verbose_name=_("tables"), null=True, blank=True, default=None)

