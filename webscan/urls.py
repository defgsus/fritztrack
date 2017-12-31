# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views

app_name = "webscan"
urlpatterns = [
    url(r'^mongodb/?$',                             views.mongodb_view,     name='mongodb'),
]