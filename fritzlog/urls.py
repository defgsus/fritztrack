# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views

app_name = "fritzlog"
urlpatterns = [
    url(r'^$',                                      views.index_view,           name='index'),
    url(r'^captures/?$',                            views.capture_sum_view,     name='captures'),
    url(r'^capture/(?P<fn>[0-9\-]+)?$',             views.capture_view,         name='capture_view'),
]