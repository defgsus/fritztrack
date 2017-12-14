# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import os
import datetime
import subprocess

from ..models import NslookupRequest, WhoisRequest, DummyLogger


def get_nslookup_raw(ip, log=None, do_read_cache=True, do_write_cache=True):
    return _lookup_impl(
        NslookupRequest,
        ["nslookup", "%s" % ip],
        ip,
        log=log, do_read_cache=do_read_cache, do_write_cache=do_write_cache
    )


def get_nslookup(ip, log=None, do_read_cache=True, do_write_cache=True):
    ret = get_nslookup_raw(ip, log=log, do_read_cache=do_read_cache, do_write_cache=do_write_cache)
    if ret is None:
        return ret
    if "\tname =" in ret:
        return ret.split("\tname =")[1].split()[0].strip(". ")
    return ret


def get_whois_row(ip, log=None, do_read_cache=True, do_write_cache=True):
    return _lookup_impl(
        WhoisRequest,
        ["whois", "%s" % ip],
        ip,
        log=log, do_read_cache=do_read_cache, do_write_cache=do_write_cache
    )


def get_whois(ip, log=None, do_read_cache=True, do_write_cache=True):
    text = get_whois_row(ip, log=log, do_read_cache=do_read_cache, do_write_cache=do_write_cache)
    if text:
        for token in ("Organization:", "descr:", "netname:", "address:", "owner:"):
            if token in text:
                return text.split(token)[1].split("\n")[0].strip()
    return text


def _lookup_impl(Model, args, ip, log=None, do_read_cache=True, do_write_cache=True):
    if do_read_cache:
        qset = Model.objects.filter(ip=ip)
        if qset.exists():
            return qset.order_by("-date")[0].response

    error = None
    try:
        res = subprocess.check_output(args)
        res = res.strip().decode("utf-8")
    except subprocess.CalledProcessError as e:
        error = e
        res = None
    except BaseException as e:
        error = e
        res = None

    if error is not None:
        if log is None:
            log = DummyLogger()
        log.error(error)

    if do_write_cache:
        Model.objects.create(
            date=datetime.datetime.now(),
            ip=ip,
            response=res,
        )
    return res


