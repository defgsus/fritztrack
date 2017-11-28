# encoding=utf-8
from __future__ import unicode_literals, print_function

import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.translation import ugettext_lazy as _


class Command(BaseCommand):
    help = _('Parse the RawLog data')

    def handle(self, *args, **options):
        starttime = datetime.datetime.now()

        from fritzlog.tools.parse_logs import parse_logs
        #from fritzlog.models import Logger

        #with Logger("get_logs") as log:
        parse_logs()

        endtime = datetime.datetime.now()
        print("TOOK %s" % (endtime - starttime))

