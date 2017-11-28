# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django.db import models
from django.utils.translation import ugettext_lazy as _


class ConnectedDevice(models.Model):
    class Meta:
        verbose_name = _("Connected Device")
        verbose_name_plural = _("Connected Devices")

    date = models.DateTimeField(verbose_name=_("date"))
    mac = models.CharField(verbose_name=_("MAC"), max_length=20)
    speed = models.IntegerField(verbose_name=_("speed"))
    signal_strength = models.IntegerField(verbose_name=_("signal strength"))

    def date_decorator(self):
        return "%s" % self.date
    date_decorator.short_description = _("date")
    date_decorator.admin_order_field = "date"

    def user_decorator(self):
        from .mapping import MacAddress
        qset = MacAddress.objects.filter(mac=self.mac)
        if qset.exists():
            return qset[0].name
        return self.mac
    user_decorator.short_description = _("name")
    user_decorator.admin_order_field = "mac"
