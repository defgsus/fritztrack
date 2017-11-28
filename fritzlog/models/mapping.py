# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django.db import models
from django.utils.translation import ugettext_lazy as _


class MacAddress(models.Model):
    class Meta:
        verbose_name = _("Mac Address")
        verbose_name_plural = _("Mac Address")

    mac = models.CharField(verbose_name=_("MAC"), max_length=20)
    name = models.CharField(verbose_name=_("name"), max_length=100)

