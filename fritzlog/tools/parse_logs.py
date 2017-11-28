# coding=utf-8
from __future__ import unicode_literals, print_function

import re
import datetime

from ..models import RawLog, DummyLogger, MacAddress, UserAction


CODE_WLAN_JOIN = "WLAN-Gerät angemeldet"
CODE_WLAN_LEAVE = "WLAN-Gerät hat sich abgemeldet"
CODE_WLAN_REMOVED = "WLAN-Gerät wurde abgemeldet"


def parse_logs(log=None):
    if log is None:
        log = DummyLogger()

    report = {
        "scanned": 0,
        "new_macs": 0,
        "failed": 0,
        "new_actions": 0,
    }

    for rawlog in RawLog.objects.all():

        # replace comma in things like '(2,4 Ghz)'
        def _repl(match):
            return "(%s.%s)" % match.groups()
        text = re.sub(r"\(([^\).]+),([^\).]+)\)", _repl, rawlog.text)

        if text.endswith("."):
            text = text[:-1]

        info = [x.strip() for x in text.split(",")]
        print(info)

        if len(info) < 1:
            continue

        def _parse_address(info, report):
            name, ip, mac = info[0:3]
            if not ip.startswith("IP") or not mac.startswith("MAC"):
                log.error("Could not parse IP/MAC for log entry pk=%s" % rawlog.pk)
                report["failed"] += 1
                return None
            ip = ip.split()[1]
            mac = mac.split()[1][:17]
            obj, created = MacAddress.objects.get_or_create(mac=mac[:20], name=name[:100])
            if created:
                report["new_macs"] += 1
            return { "name": name, "ip": ip, "mac": mac }

        def _add_action(address, action):
            obj, created = UserAction.objects.get_or_create(
                date=rawlog.date,
                mac=address["mac"],
                ip=address["ip"],
                action=action,
            )
            if created:
                report["new_actions"] += 1

        code = info[0]
        if code.startswith(CODE_WLAN_JOIN):
            if len(info) >= 4:
                address = _parse_address(info[2:5], report)
                if address is None:
                    continue
                _add_action(address, UserAction.ACT_WLAN_CONNECT)

        elif code.startswith(CODE_WLAN_LEAVE) or code.startswith(CODE_WLAN_REMOVED):
            if len(info) >= 4:
                address = _parse_address(info[1:4], report)
                if address is None:
                    continue
                _add_action(address, UserAction.ACT_WLAN_DISCONNECT)

    log.log("%(new_macs)s new MACs, %(new_actions)s new user-actions" % report)



