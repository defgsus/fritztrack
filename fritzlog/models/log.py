# coding=utf-8
from __future__ import unicode_literals, print_function

import traceback

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Log(models.Model):
    """Simple database log"""

    class Meta:
        verbose_name = _("Worker Log")
        verbose_name_plural = _("Worker Logs")

    name = models.CharField(verbose_name=_("name"), max_length=100, editable=False, default="", db_index=True)
    count = models.BigIntegerField(verbose_name=_("count"), editable=False, default=0, db_index=True)
    date_started = models.DateTimeField(verbose_name=_("started"), default=timezone.now, db_index=True)
    date_finished = models.DateTimeField(verbose_name=_("finished"), default=None, null=True, blank=True, db_index=True)
    duration = models.DurationField(verbose_name=_("duration"), default=None, null=True, blank=True, db_index=True)
    log_text = models.TextField(verbose_name=_("log"), default=None, null=True, blank=True)
    error_text = models.TextField(verbose_name=_("error"), default=None, null=True, blank=True)

    @classmethod
    def start_log(cls, name):
        now = timezone.now()
        count = cls.objects.filter(name=name).count() + 1
        print("\n%s.%s started @ %s" % (name, count, now))
        return cls.objects.create(name=name, count=count, date_started=now)

    def finish(self, exception_or_error=None):
        self.date_finished = timezone.now()
        self.duration = self.date_finished - self.date_started
        if exception_or_error is not None:
            if self.error_text:
                self.error_text = "%s\n%s" % (self.error_text, exception_or_error)
            else:
                self.error_text = "%s" % exception_or_error
        self.save()
        if self.log_text:
            print("LOG: %s" % self.log_text)
        if self.error_text:
            print("ERROR: %s" % self.error_text)
        print("%s finished after %s" % (self.name, self.duration))


class Logger(object):
    """
    Automatic database logging,
    also catches exceptions and stores them in DB

    with Logger("my_task") as log:
        if not the_task():
            log.error("some error")
        log.log("some info")
        raise RuntimeError("will be logged")
    """
    def __init__(self, name):
        self._name = name
        self._log_lines = []
        self._error_lines = []
        self._context = []
        self.log_db = None

    def __enter__(self):
        self.log_db = Log.start_log(self._name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._log_lines:
            self.log_db.log_text = "\n".join(self._log_lines)
        if self._error_lines:
            self.log_db.error_text = "\n".join(self._error_lines)
        if exc_val and exc_tb:
            exc_val = "%s%s\n%s\n%s" % (self.context(), exc_type, exc_val, traceback.format_tb(exc_tb))
        self.log_db.finish(exc_val)
        return True

    def push(self, context_name):
        self._context.append("%s" % context_name)

    def pop(self):
        self._context = self._context[:-1]

    def context(self):
        ctx = []
        for c in self._context:
            if not ctx or ctx[-1] != c:
                ctx.append(c)
        ret = ":".join(ctx)
        if ret:
            ret += ": "
        return ret

    def log(self, line):
        line = self.context() + ("%s" % line).strip()
        print("LOG: %s" % line)
        self._log_lines.append(line)

    def error(self, line):
        line = self.context() + ("%s" % line).strip()
        print("ERR: %s" % line)
        self._error_lines.append(line)



class DummyLogger(object):
    """

    with DummyLogger("my_task") as job:
        the_task()
        job.log("some_info")
    """
    def __init__(self, name=""):
        self._name = name
        self._context = []

    def push(self, context_name):
        self._context.append("%s" % context_name)

    def pop(self):
        self._context = self._context[:-1]

    def log(self, line):
        print("LOG:%s: %s" % (self._name, line))

    def error(self, line):
        print("ERR:%s: %s" % (self._name, line))



class LoggerContext(object):
    """
    Scoped context change for a Logger instance
    
    with Logger("my_task") as log:
        with LoggerContext(log, "task_1"):
            the_task_1(log)
        with LoggerContext(log, "task_2"):
            the_task_2(log)
    """
    def __init__(self, log, name):
        self._log = log
        self._name = name

    def __enter__(self):
        self._log.push(self._name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._log.pop()
