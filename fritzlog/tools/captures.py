# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import os
import datetime
import pyshark

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from ..models import ConnectedDevice, MacAddress, GeoIp, DnsResponse, Capture


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


def parse_and_store_capture_ips(capture, mapping=None):
    print("parsing")
    if mapping is None:
        from .mapping import Mapping
        mapping = Mapping()
    for pkt in capture:

        if hasattr(pkt, "ip"):
            # TODO: quick hack to check for device ip
            if pkt.ip.src.startswith("192.168.178"):
                ip, dst = pkt.ip.src, pkt.ip.dst
            else:
                ip, dst = pkt.ip.dst, pkt.ip.src
            mapping.ip_to_url(dst)

            if hasattr(pkt.ip, "geoasnum") and pkt.ip.geoasnum:
                mapping.store_geo_ip(
                    ip=dst,
                    asnum=pkt.ip.get_field("geodst_asnum"),
                    city=pkt.ip.get_field("geodst_city"),
                    country=pkt.ip.get_field("geodst_country"),
                    lat=pkt.ip.get_field("geodst_lat"),
                    lon=pkt.ip.get_field("geodst_lon"),
                )

    print(mapping._ip2url)


def scan_dns_pakets(capture):
    num_created = 0
    for pkt in capture:
        if pkt.highest_layer == "DNS":
            qry, alias, ip = pkt.dns.get("qry_name"), pkt.dns.get("cname"), pkt.dns.get("a")
            if qry is not None and ip is not None:
                kwargs = dict(query_name=qry, cname=alias, ip=ip)
                if not DnsResponse.objects.filter(**kwargs).exists():
                    kwargs["date"] = pkt.sniff_time
                    DnsResponse.objects.create(**kwargs)
                    num_created += 1
    return num_created


def get_connections(capture):
    """
    ip.src -> dict((protocol,port,ip.dst) -> count)
    
    """
    ip_dict = dict()
    for pkt in capture:

        if not hasattr(pkt, "ip") and not hasattr(pkt, "ipv6"):
            continue

        protocol = pkt.highest_layer

        tcp_dst_port = None
        tcp_src_port = None
        if hasattr(pkt, "tcp"):
            tcp_src_port = pkt.tcp.srcport
            tcp_dst_port = pkt.tcp.dstport

        if hasattr(pkt, "ip"):
            if pkt.ip.src.startswith("192.168.178"):
                ip, dst = pkt.ip.src, pkt.ip.dst
            else:
                ip, dst = pkt.ip.dst, pkt.ip.src
                tcp_dst_port = tcp_src_port
        else:
            # TODO: how to discern src and dst in IPv6?
            ip, dst = pkt.ipv6.src, pkt.ipv6.dst

        ip = "%s" % ip
        dkey = (
            "%s" % protocol,
            int(tcp_dst_port) if tcp_dst_port else None,
            "%s" % dst
        )
        if ip not in ip_dict:
            ip_dict[ip] = {dkey: 1}
        else:
            ip_dict[ip][dkey] = ip_dict[ip].get(dkey, 0) + 1
    return ip_dict


def get_all_connections():
    ip_dict = dict()
    qset = Capture.objects.all().exclude(connections=None)
    for cap in qset:
        cons = cap.connections
        for ip in cons:
            if ip not in ip_dict:
                ip_dict[ip] = cons[ip]
            else:
                for dkey in cons[ip]:
                    ip_dict[ip][dkey] = ip_dict[ip].get(dkey, 0) + cons[ip][dkey]
    return ip_dict
