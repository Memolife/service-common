# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from urlparse import urlparse
from flask import Flask
from mongokit import Connection
try:
    import simplejson as json
except ImportError:
    import json
import datetime
from bson.objectid import ObjectId

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object('config')

connection = Connection(app.config['MONGODB_URL'])

def get_connection():
    return connection

def get_database():
    db_name = urlparse(app.config['MONGODB_URL']).path[1:]
    return get_connection()[db_name]



class MongoJsonEncoder(json.JSONEncoder):
    """ Serializer for mongo objects.
    Usage:
        json.dumps(doc, cls=MongoJsonEncoder)
    In flask:
        app = Flask(__name__)
        app.json_encoder = MongoJsonEncoder
    """
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return unicode(obj)
        return json.JSONEncoder.default(self, obj)


