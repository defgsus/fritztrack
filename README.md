# Owning the Fritz!Box with Django

Simple Django project to frequently collect data
from the FritzBox router and store to DB

Uses selenium with PhantomJS for the web interface,
fritzconnection for the AVM tr-064 soap interface
and django-kronos for the cron-job integration

Django Admin is used to browse the data.

## Dependencies

- Python 2.7, Django 1.11, fritzconnection 0.6.5
- phantomjs webdriver binary
- tshark and pyshark (for basic analysis of captured packets)
- testet with Fritz!Box 7490, Fritz!OS 6.90 (**german**)

## How to run

```bash
./manage.py installtasks
```
to install the `fritz_worker` cronjob,

or manually
```bash
./manage.py runtask fritz_worker      # to run all
./manage.py fritz_get_logs            # get log files
./manage.py fritz_get_connected       # get connected devices
./manage.py fritz_capture [seconds]   # capture packets
```

### What it does

At defined intervals (see `fritzlog/cron.py`),
- It captures the log entries from the web interface
- Stores the currently connected WLAN devices (with signal strength)
- Captures a few seconds of the IP-traffic and dumps it to disk

Yes, this is evil. Please make sure you have the right mindset before use.


