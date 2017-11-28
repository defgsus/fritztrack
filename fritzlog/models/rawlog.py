# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django.db import models
from django.utils.translation import ugettext_lazy as _


class RawLog(models.Model):
    class Meta:
        verbose_name = _("Raw Log")
        verbose_name_plural = _("Raw Logs")

    date = models.DateTimeField(verbose_name=_("date"))
    text = models.CharField(verbose_name=_("text"), max_length=2000)

    def date_decorator(self):
        return "%s" % self.date
    date_decorator.short_description = _("date")
    date_decorator.admin_order_field = "date"

