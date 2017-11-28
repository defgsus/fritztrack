# coding=utf-8
from __future__ import unicode_literals, print_function

import datetime

from .fritz_browser import FritzBrowser
from ..models import RawLog, DummyLogger


def get_logs(browser=None, log=None):
    if log is None:
        log = DummyLogger()

    if browser is None:
        log.log("creating browser")
        browser = FritzBrowser()
        browser.login()

    browser.open_log()
    logs = browser.get_log_strings()

    num_logs, num_created = 0, 0
    for logtext in reversed(logs):
        date, time, text = logtext.split("\n")

        date = date.split(".")
        time = time.split(":")
        # do not check for seconds
        # because for some reason the fritzbox log seems to change them
        dt = datetime.datetime(2000+int(date[2]), int(date[1]), int(date[0]),
                               int(time[0]), int(time[1]), 0)

        text = text[:2000].strip()
        num_logs += 1

        if RawLog.objects.filter(date=dt, text=text).exists():
            continue
        RawLog.objects.create(date=dt, text=text)
        num_created += 1

    log.log("%s found, %s new" % (num_logs, num_created))

