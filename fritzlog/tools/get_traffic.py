# coding=utf-8
from __future__ import unicode_literals, print_function

import datetime

from .fritz_browser import FritzBrowser
from ..models import RawLog, DummyLogger



def get_traffic(browser=None, log=None):
    if log is None:
        log = DummyLogger()

    if browser is None:
        log.log("creating browser")
        browser = FritzBrowser()
        browser.login()

    browser.open_capture()

    table = browser.driver.find_element_by_css_selector("table.zebra")
    trs = table.find_elements_by_tag_name("tr")
    for tr in trs:
        if "1. Internetverbindung" in tr.text:
            start_button = tr.find_element_by_css_selector('button[name="start"]')



