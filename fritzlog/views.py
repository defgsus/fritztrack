# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import os
import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from tools import captures


def index_view(request):
    return HttpResponseRedirect(reverse("admin:index"))


def capture_list(request):
    capture_list = captures.get_all_captures()
    capture_list.sort(key=lambda x: x["date"], reverse=True)
    ctx = {
        "capture_list": capture_list,
    }
    return render(request, "fritzlog/capture_list.html", ctx)


def capture_view(request, fn):
    filename = os.path.join(settings.MEDIA_ROOT, "capture", fn[:10], "%s.eth" % fn)
    capture = captures.open_capture(filename)

    cons = captures.get_connections(capture)
    connection_list = []
    for ip in sorted(cons):
        dst = cons[ip]
        connection_list.append((
            captures.ip_to_name(ip),
            [(dst[i], i) for i in sorted(dst, key=lambda x: -dst[x])],
        ))

    ctx = {
        "connection_list": connection_list,
    }
    return render(request, "fritzlog/capture_view.html", ctx)
