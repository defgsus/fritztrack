# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django.contrib import admin

from .models import *


class LogAdmin(admin.ModelAdmin):
    list_display = ("name", "count", "date_started", "date_finished", "duration", "log_text", "error_text")
    ordering = ("-date_finished", )


class RawLogAdmin(admin.ModelAdmin):
    list_display = ("id", "date_decorator", "text")
    ordering = ("-date",)


class MacAddressAdmin(admin.ModelAdmin):
    list_display = ("mac", "name")
    ordering = ("mac", )


class UserActionAdmin(admin.ModelAdmin):
    list_display = ("date_decorator", "mac", "user_decorator", "ip", "action")
    ordering = ("-date", )


admin.site.register(Log, LogAdmin)
admin.site.register(RawLog, RawLogAdmin)
admin.site.register(MacAddress, MacAddressAdmin)
admin.site.register(UserAction, UserActionAdmin)
