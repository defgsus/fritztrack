# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import os

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.urls import reverse

from picklefield import PickledObjectField


class Capture(models.Model):
    class Meta:
        verbose_name = _("Capture")
        verbose_name_plural = _("Captures")

    date = models.DateTimeField(verbose_name=_("date"))
    seconds = models.IntegerField(verbose_name=_("length in seconds"))
    filename = models.CharField(verbose_name=_("filename"), max_length=50)
    size = models.BigIntegerField(verbose_name=_("filesize"))

    is_parsed = models.BooleanField(verbose_name=_("is parsed"), default=False)

    connections = PickledObjectField(verbose_name=_("connections"), default=None, null=True, blank=True)

    def full_filename(self):
        return os.path.join(settings.MEDIA_ROOT, "capture", self.filename[:10], self.filename)

    def file_url(self):
        return "%scapture/%s/%s" % (settings.MEDIA_URL, self.filename[:10], self.filename)

    def show_url(self):
        return reverse("fritzlog:capture_view", args=(self.filename[:19],))

    def date_decorator(self):
        return "%s" % self.date
    date_decorator.short_description = _("date")

    def filename_decorator(self):
        return """<a href="%s">%s</a> (<a href="%s">%s</a>)""" % (
            self.show_url(),
            self.filename,
            self.file_url(),
            _("download"),
        )
    filename_decorator.short_description = _("filename")
    filename_decorator.allow_tags = True
