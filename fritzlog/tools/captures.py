# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import os
import datetime
import pyshark

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from ..models import ConnectedDevice, MacAddress


def get_all_captures():
    captures = []
    for root, dirs, files in os.walk(os.path.join(settings.MEDIA_ROOT, "capture")):
        for fn in files:
            dt = datetime.datetime.strptime(fn[:19], "%Y-%m-%d-%H-%M-%S")
            file_url = "%scapture/%s/%s" % (settings.MEDIA_URL, fn[:10], fn)
            show_url = reverse("fritzlog:capture_view", args=(fn[:19],))
            captures.append({
                "date": dt,
                "filename": os.path.join(root, fn),
                "short_filename": fn,
                "file_url": file_url,
                "view_url": show_url,
            })
    return captures


def open_capture(filename):
    return pyshark.FileCapture(filename)


def ip_to_name(ip, date=None):
    if date is None:
        qset = ConnectedDevice.objects.filter(ip=ip)
    else:
        qset = ConnectedDevice.objects.filter(ip=ip, date__lte=date)
    if qset.exists():
        mac = qset.order_by("-date")[0].mac
        qset = MacAddress.objects.filter(mac=mac)
        if qset.exists():
            return qset[0].name
        return mac
    return ip


def get_connections(capture):
    ip_dict = dict()
    for pkt in capture:
        if not hasattr(pkt, "ip"):
            continue

        if pkt.ip.src.startswith("192.168.178"):
            ip, dst = pkt.ip.src, pkt.ip.dst
        else:
            ip, dst = pkt.ip.dst, pkt.ip.src

        if hasattr(pkt.ip, "geoasnum") and pkt.ip.geoasnum:
            dst += " (%s)" % pkt.ip.geoasnum

        if ip not in ip_dict:
            ip_dict[ip] = {dst: 1}
        else:
            if dst not in ip_dict[ip]:
                ip_dict[ip][dst] = 1
            else:
                ip_dict[ip][dst] += 1
    return ip_dict