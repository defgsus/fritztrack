# encoding=utf-8
from __future__ import unicode_literals, print_function

import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.translation import ugettext_lazy as _


class Command(BaseCommand):
    help = _('Get the currently connected WLAN devices')

    def handle(self, *args, **options):
        starttime = datetime.datetime.now()

        from fritzlog.tools.get_connected import get_connected
        from fritzlog.models import Logger

        with Logger("get_connected") as log:
            get_connected(log=log)

        endtime = datetime.datetime.now()
        print("TOOK %s" % (endtime - starttime))

