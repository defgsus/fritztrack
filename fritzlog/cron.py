# encoding:utf-8

# see https://github.com/jgorset/django-kronos

from __future__ import unicode_literals, print_function

import kronos

from .models import Logger, LoggerContext
from .tools.fritz_browser import FritzBrowser
from .tools.get_logs import get_logs
from .tools.get_connected import get_connected
from .tools.get_traffic import get_traffic


@kronos.register("0 * * * *")
def fritz_worker():
    """
    Do all the fritz scraping
    """
    with Logger("fritz_worker") as log:
        browser = FritzBrowser()
        with LoggerContext(log, "get_logs"):
            browser.login()
            get_logs(browser=browser, log=log)
        with LoggerContext(log, "get_connected"):
            get_connected(log=log)
        with LoggerContext(log, "get_traffic"):
            get_traffic(num_seconds=25, browser=browser, log=log)
