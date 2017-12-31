# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import json
import datetime
from pymongo.collection import ObjectId

from django.shortcuts import render

from webscan.tools.mongo import scan_for_mongodb, get_mongodb_detail


class MongoSerializer(json.JSONEncoder):
    def default(self, obj):
        try:
            return super(MongoSerializer, self).default(obj)
        except TypeError:
            return "%s" % obj

def mongodb_view(request):

    host = request.GET.get("host")
    port = request.GET.get("port")
    database_name = request.GET.get("database")
    collection_name = request.GET.get("collection")

    ctx = {
        "host": host or "",
        "port": port or "27017",
        "database_name": database_name or "",
        "collection_name": collection_name or "",
    }

    if host and port:
        model = scan_for_mongodb(host, int(port))
        ctx["model"] = model

        if database_name and collection_name:
            detail = get_mongodb_detail(host, int(port), database_name, collection_name)
            if isinstance(detail, (list, dict)):
                detail = json.dumps(detail, indent=4, sort_keys=True, cls=MongoSerializer)
            ctx["detail"] = detail
    return render(request, "webscan/mongodb.html", ctx)

