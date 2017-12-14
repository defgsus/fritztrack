# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import os
import datetime


from .nslookup import get_nslookup, get_whois
from ..models import MacAddress, GeoIp, DnsResponse


class Mapping(object):

    def __init__(self):
        self._ip2url = dict()
        self._ip2owner = dict()
        self._ip2geo = dict()

    def ip_to_url(self, ip):
        if ip not in self._ip2url:
            qset = DnsResponse.objects.filter(ip=ip)
            if qset.exists():
                dns = qset.order_by("-date")[0]
                self._ip2url[ip] = dns.cname or dns.query_name
            else:
                self._ip2url[ip] = get_nslookup(ip)
        return self._ip2url[ip]

    def ip_to_owner(self, ip):
        if ip not in self._ip2owner:
            self._ip2owner[ip] = get_whois(ip)
        return self._ip2owner[ip]

    def ip_to_geo(self, ip):
        if ip not in self._ip2geo:
            qset = GeoIp.objects.filter(ip=ip)
            if not qset.exists():
                self._ip2geo[ip] = None
            else:
                geo = qset.order_by("-date")[0]
                self._ip2geo[ip] = {
                    "asnum": geo.asnum,
                    "lat": geo.lat,
                    "lon": geo.lon,
                    "city": geo.city,
                    "country": geo.country,
                }
        return self._ip2geo[ip]

    def store_geo_ip(self, ip, asnum, city, country, lat, lon):
        if ip in self._ip2geo or GeoIp.objects.filter(ip=ip).exists():
            return
        geo = GeoIp.objects.create(
            date=datetime.datetime.now(),
            ip=ip,
            asnum=asnum,
            city=city,
            country=country,
            lat=lat,
            lon=lon,
        )
        self._ip2geo = {
            "asnum": geo.asnum,
            "lat": geo.lat,
            "lon": geo.lon,
            "city": geo.city,
            "country": geo.country,
        }

    def ip_decorator(self, ip):
        ret = "%s" % ip
        url = self.ip_to_url(ip)
        if url:
            ret += " (<b>%s</b>)" % url

        owner = self.ip_to_owner(ip)
        if owner:
            ret += " (%s)" % owner

        geo = self.ip_to_geo(ip)
        if geo:
            if geo["asnum"]:
                ret += " (%s" % geo["asnum"]
            if geo["country"]:
                ret += "/%s" % geo["country"]
            ret += ")"

        return ret
