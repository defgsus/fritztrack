# encoding=utf-8
from __future__ import unicode_literals, print_function

import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.translation import ugettext_lazy as _


class Command(BaseCommand):
    help = _('Capture some traffic from Fritzbox')

    def add_arguments(self, parser):
        parser.add_argument('seconds', type=int, nargs="?", default=10,
                            help="Number of seconds to capture")

    def handle(self, *args, **options):
        starttime = datetime.datetime.now()

        from fritzlog.tools.get_traffic import get_traffic
        from fritzlog.models import Logger

        with Logger("get_logs") as log:
            get_traffic(num_seconds=options["seconds"], log=log)

        endtime = datetime.datetime.now()
        print("TOOK %s" % (endtime - starttime))

