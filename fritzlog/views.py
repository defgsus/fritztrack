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
from tools.mapping import Mapping
from .models import Capture


def index_view(request):
    return HttpResponseRedirect(reverse("admin:index"))


# NOT USED
def capture_list(request):
    capture_list = captures.get_all_captures()
    capture_list.sort(key=lambda x: x["date"], reverse=True)
    ctx = {
        "capture_list": capture_list,
    }
    return render(request, "fritzlog/capture_list.html", ctx)


def get_connection_list(cons, mapping=None):
    if mapping is None:
        mapping = Mapping()
    connection_list = []
    for ip in sorted(cons):
        con_map = cons[ip]

        ip_cnt = dict()
        for ikey in con_map:
            ip_cnt[ikey[2]] = ip_cnt.get(ikey[2], 0) + con_map[ikey]

        first_row = True
        for dst_ip in sorted(ip_cnt, key=lambda k: -ip_cnt[k]):
            con_keys = sorted(con_map, key=lambda k: -con_map[k])
            for ikey in con_keys:
                if ikey[2] == dst_ip:
                    row = [captures.ip_to_name(ip) if first_row else ""]
                    first_row = False
                    row.append("%sx" % con_map[ikey])
                    for val in ikey[:-1]:
                        row.append(val if val else "")
                    row.append(mapping.ip_decorator(ikey[-1]))
                    connection_list.append(row)
    return connection_list


def capture_view(request, fn):
    filename = os.path.join(settings.MEDIA_ROOT, "capture", fn[:10], "%s.eth" % fn)
    try:
        capture_db = Capture.objects.get(filename="%s.eth" % fn)
    except Capture.DoesNotExist:
        capture_db = None

    capture = captures.open_capture(filename)

    mapping = Mapping()
    if capture_db:
        if not capture_db.connections:
            #captures.parse_and_store_capture_ips(capture, mapping)
            capture_db.connections = captures.get_connections(capture)
            capture_db.save()
        cons = capture_db.connections
    else:
        cons = captures.get_connections(capture)

    connection_list = get_connection_list(cons, mapping)

    ctx = {
        "capture": capture_db,
        "connection_list": connection_list,
    }
    return render(request, "fritzlog/capture_view.html", ctx)


def capture_sum_view(request):

    connection_list = get_connection_list(captures.get_all_connections())

    ctx = {
        "connection_list": connection_list,
    }
    return render(request, "fritzlog/capture_view.html", ctx)
