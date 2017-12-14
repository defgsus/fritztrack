# coding=utf-8
from __future__ import unicode_literals, print_function

import re
import datetime

from ..models import Capture, DummyLogger, MacAddress, UserAction
from .captures import open_capture, scan_dns_pakets, get_connections, parse_and_store_capture_ips
from .mapping import Mapping


def parse_captures(log=None):
    if log is None:
        log = DummyLogger()

    report = {
        "parsed": 0,
        "new_dns": 0,
    }

    #mapping = Mapping()
    for capture_db in Capture.objects.filter(is_parsed=False):
        capture = open_capture(capture_db.full_filename())

        num_new_dns = scan_dns_pakets(capture)

        cons = get_connections(capture)

        capture_db.is_parsed = True
        capture_db.connections = cons
        capture_db.save()

        report["parsed"] += 1
        report["new_dns"] += num_new_dns
        log.log("scanned %s, %s new dns" % (capture_db.filename, num_new_dns))

    log.log("%(parsed)s parsed, %(new_dns)s new dns" % report)



