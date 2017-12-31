
from django.utils import timezone

from pymongo import MongoClient
from ..models import MongoDbConnection



def scan_for_mongodb(host, port=27017):
    today = timezone.now().replace(microsecond=0)
    qset = MongoDbConnection.objects.filter(host=host, port=port)
    if qset.exists():
        return qset.order_by("-date")[0]

    try:
        client = MongoClient(host, port=port)

        databases = []

        dbinfos = list(client.list_databases())

        for dbinfo in dbinfos:
            databases.append(dbinfo.copy())
            try:
                db = client.get_database(dbinfo["name"])
                colinfos = list(db.list_collections())
                databases[-1]["collections"] = colinfos
            except ValueError as e:
                databases[-1]["error"] = "%s" % e

        model = MongoDbConnection.objects.create(
            host=host,
            port=port,
            date=today,
            data=databases
        )
    except ValueError as e:
        model = MongoDbConnection.objects.create(
            host=host,
            port=port,
            date=today,
            is_error=True,
            data={"error": "%s" % e}
        )

    return model


def get_mongodb_detail(host, port, database_name, collection_name):
    try:
        client = MongoClient(host, port=port)

        db = client.get_database(database_name)
        col = db.get_collection(collection_name)
        return list(col.find()[:10])

    except ValueError as e:
        return "%s" % e