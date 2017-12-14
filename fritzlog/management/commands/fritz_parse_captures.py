# encoding=utf-8
from __future__ import unicode_literals, print_function

import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.translation import ugettext_lazy as _


class Command(BaseCommand):
    help = _('Parse all (new) capture files and store everything to db')

    def handle(self, *args, **options):
        starttime = datetime.datetime.now()

        from fritzlog.tools.parse_captures import parse_captures
        from fritzlog.models import Logger

        with Logger("parse_captures") as log:
            parse_captures(log)

        endtime = datetime.datetime.now()
        print("TOOK %s" % (endtime - starttime))

