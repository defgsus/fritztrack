# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django.contrib import admin

from .models import *


class LogAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "count", "date_started", "date_finished", "duration", "log_text", "error_text")
    ordering = ("-date_finished", )


class RawLogAdmin(admin.ModelAdmin):
    list_display = ("id", "date_decorator", "text")
    ordering = ("-date",)


class MacAddressAdmin(admin.ModelAdmin):
    list_display = ("id", "mac", "name")
    ordering = ("mac", )


class UserActionAdmin(admin.ModelAdmin):
    list_display = ("id", "date_decorator", "mac", "user_decorator", "ip", "action")
    ordering = ("-date", )


class ConnectedDeviceAdmin(admin.ModelAdmin):
    list_display = ("id", "date_decorator", "mac", "ip", "user_decorator", "speed", "signal_strength")
    ordering = ("-date", )


class CaptureAdmin(admin.ModelAdmin):
    list_display = ("id", "date_decorator", "seconds", "size", "filename_decorator")
    ordering = ("-date", )


admin.site.register(Log, LogAdmin)
admin.site.register(RawLog, RawLogAdmin)
admin.site.register(MacAddress, MacAddressAdmin)
admin.site.register(UserAction, UserActionAdmin)
admin.site.register(ConnectedDevice, ConnectedDeviceAdmin)
admin.site.register(Capture, CaptureAdmin)

