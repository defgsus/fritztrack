# encoding:utf-8

# see https://github.com/jgorset/django-kronos

from __future__ import unicode_literals, print_function

import kronos

from .models import Logger, LoggerContext
from .tools.get_logs import get_logs


@kronos.register("37 * * * *")
def fritz_worker():
    """
    Do all the fritz scraping
    """
    with Logger("fritz_worker") as log:
        with LoggerContext(log, "get_logs"):
            get_logs(log=log)
