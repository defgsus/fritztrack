# Fritzbox analysis via Django

Simple Django project to frequently collect log files
from the FritzBox router and store to DB

Uses selenium with PhantomJS for the web interface
and django-kronos for the cron-job integration

## dependencies

Python 2.7, Django 1.11, fritzconnection 0.6.5

phantomjs webdriver binary

Testet with Fritz!Box 7490, Fritz!OS 6.90 (**german**)

## how to run

```bash
./manage.py installtasks
```
to install the `fritz_worker` cronjob, or manually
```bash
./manage.py runtask fritz_worker
```
