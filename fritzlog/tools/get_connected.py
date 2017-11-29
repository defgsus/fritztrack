# coding=utf-8
from __future__ import unicode_literals, print_function

import datetime

import fritzconnection

from ..models import RawLog, DummyLogger, ConnectedDevice
from .fritzbox_credentials import LOGIN_PASSWORD

def get_connected(log=None):
    if log is None:
        log = DummyLogger()

    now = datetime.datetime.now().replace(microsecond=0)

    con = fritzconnection.FritzConnection(password=LOGIN_PASSWORD)

    res = con.call_action("WLANConfiguration", "GetTotalAssociations")
    num_devices = res["NewTotalAssociations"]
    num_stored = 0
    for i in range(num_devices):
        res = con.call_action("WLANConfiguration", "GetGenericAssociatedDeviceInfo",
                              NewAssociatedDeviceIndex=i)

        obj, created = ConnectedDevice.objects.get_or_create(
            date=now,
            mac=res["NewAssociatedDeviceMACAddress"].upper(),
            ip=res["NewAssociatedDeviceIPAddress"],
            speed=res["NewX_AVM-DE_Speed"],
            signal_strength=res["NewX_AVM-DE_SignalStrength"],
        )
        if created:
            num_stored += 1

    log.log("%s devices, %s stored" % (num_devices, num_stored))
