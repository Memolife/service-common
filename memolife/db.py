# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from urlparse import urlparse
from flask import Flask
from mongokit import Connection

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object('config')

connection = Connection(app.config['MONGODB_URL'])

def get_connection():
    return connection

def get_database():
    db_name = urlparse(app.config['MONGODB_URL']).path[1:]
    return get_connection()[db_name]

