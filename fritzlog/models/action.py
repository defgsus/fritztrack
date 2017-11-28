# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserAction(models.Model):

    ACT_WLAN_CONNECT = "wlan-connect"
    ACT_WLAN_DISCONNECT = "wlan-disconnect"

    ACTION_CHOICES = (
        (ACT_WLAN_CONNECT, _("connect wlan")),
        (ACT_WLAN_DISCONNECT, _("disconnect wlan")),
    )

    class Meta:
        verbose_name = _("User Action")
        verbose_name_plural = _("User Actions")

    date = models.DateTimeField(verbose_name=_("date"))
    mac = models.CharField(verbose_name=_("MAC"), max_length=20)
    ip = models.CharField(verbose_name=_("IP"), max_length=20)
    action = models.CharField(verbose_name=_("action"), max_length=50,
                              choices=ACTION_CHOICES)

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