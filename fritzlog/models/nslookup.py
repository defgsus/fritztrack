# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django.db import models
from django.utils.translation import ugettext_lazy as _


def linebreaks(text):
    if not text:
        return text
    lines = text.split("\n")
    return "<br/>".join("<nobr>%s</nobr>" % l for l in lines)


class WhoisRequest(models.Model):

    class Meta:
        verbose_name = _("Whois Requests")
        verbose_name_plural = _("Whois Requests")

    date = models.DateTimeField(verbose_name=_("date"))
    ip = models.CharField(verbose_name=_("IP"), max_length=40)
    response = models.TextField(verbose_name=_("response"), null=True, blank=True, default=None)

    def date_decorator(self):
        return "%s" % self.date.replace(microsecond=0)
    date_decorator.short_description = _("date")
    date_decorator.admin_order_field = "date"

    def response_decorator(self):
        return linebreaks(self.response)
    response_decorator.short_description = _("response")
    response_decorator.admin_order_field = "response"
    response_decorator.allow_tags = True


class NslookupRequest(models.Model):

    class Meta:
        verbose_name = _("Nslookup Requests")
        verbose_name_plural = _("Nslookup Requests")

    date = models.DateTimeField(verbose_name=_("date"))
    ip = models.CharField(verbose_name=_("IP"), max_length=40)
    response = models.TextField(verbose_name=_("response"), null=True, blank=True, default=None)

    def date_decorator(self):
        return "%s" % self.date.replace(microsecond=0)
    date_decorator.short_description = _("date")
    date_decorator.admin_order_field = "date"

    def response_decorator(self):
        return linebreaks(self.response)
    response_decorator.short_description = _("response")
    response_decorator.admin_order_field = "response"
    response_decorator.allow_tags = True


class GeoIp(models.Model):

    class Meta:
        verbose_name = _("GeoIP")
        verbose_name_plural = _("GeoIPs")

    date = models.DateTimeField(verbose_name=_("date"))
    ip = models.GenericIPAddressField(verbose_name=_("IP"))
    asnum = models.CharField(verbose_name=_("asnum"), max_length=50, null=True, blank=True)
    city = models.CharField(verbose_name=_("city"), max_length=50, null=True, blank=True)
    country = models.CharField(verbose_name=_("country"), max_length=50, null=True, blank=True)
    lat = models.DecimalField(verbose_name=_("lat"), max_digits=15, decimal_places=10, null=True, blank=True)
    lon = models.DecimalField(verbose_name=_("lon"), max_digits=15, decimal_places=10, null=True, blank=True)

    def date_decorator(self):
        return "%s" % self.date.replace(microsecond=0)
    date_decorator.short_description = _("date")
    date_decorator.admin_order_field = "date"



class DnsResponse(models.Model):

    class Meta:
        verbose_name = _("DNS Response")
        verbose_name_plural = _("DNS Responses")

    date = models.DateTimeField(verbose_name=_("date"))
    ip = models.GenericIPAddressField(verbose_name=_("IP"))
    query_name = models.CharField(verbose_name=_("query"), max_length=200)
    cname = models.CharField(verbose_name=_("alias"), max_length=200, null=True, blank=True)

    def date_decorator(self):
        return "%s" % self.date.replace(microsecond=0)
    date_decorator.short_description = _("date")
    date_decorator.admin_order_field = "date"
