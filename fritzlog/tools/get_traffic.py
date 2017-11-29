# coding=utf-8
from __future__ import unicode_literals, print_function

import os
import datetime
import threading
import requests

from django.conf import settings

from .fritz_browser import FritzBrowser
from ..models import RawLog, DummyLogger



def get_traffic(num_seconds=10, browser=None, log=None):
    if log is None:
        log = DummyLogger()

    if browser is None:
        log.log("creating browser")
        browser = FritzBrowser()

    browser.open_capture()

    # http://fritz.box/cgi-bin/capture_notimeout?sid=f92882de0cc85624&capture=Start&snaplen=1600&ifaceorminor=3-0

    start_url = browser.get_capture_url()
    stop_url = browser.get_capture_stop_url()
    filepath = os.path.join(
        settings.MEDIA_ROOT, "capture", "%s" % datetime.date.today()
    )
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    now_str = ("%s" % datetime.datetime.now().replace(microsecond=0)).replace(":", "-").replace(" ", "-")
    filename = os.path.join(filepath, ("%s.eth" % now_str))

    thread = threading.Thread(target=lambda: _store_capture(start_url, filename, log))
    log.log("starting capture thread")
    thread.start()
    browser.sleep(num_seconds)
    requests.get(stop_url)
    if thread.is_alive():
        thread.join()

    return

    table = browser.driver.find_element_by_css_selector("table.zebra")
    trs = table.find_elements_by_tag_name("tr")
    for tr in trs:
        #if "1. Internetverbindung" in tr.text:
        if "Routing-Schnittstelle" in tr.text:
            start_button = tr.find_element_by_css_selector('button[name="start"]')

            thread = threading.Thread(target=lambda: _store_capture(start_url, filename, log))
            log.log("starting capture thread")
            thread.start()
            log.log("waiting")
            browser.sleep(4)
            log.log("stopping")
            stop_button = tr.find_element_by_css_selector('button[name="stop"]')
            stop_button.click()
            #requests.get(stop_url)
            if thread.is_alive():
                thread.join()


def _store_capture(url, filename, log):
    res = requests.get(url)
    with open(filename, b"wb") as f:
        f.write(res.content)
    log.log("stored %s bytes" % len(res.content))
