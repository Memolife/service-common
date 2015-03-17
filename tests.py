# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import unittest
from flask import Flask, make_response
import jwt
from memolife.auth import is_authenticated

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object('config')

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        token = create_token({
            '_id': "testuserid",
            'email': 'test@test.com',
            'roles': ['user']
        })
        self.bearer_header = "Bearer {0}".format(token)
        self.app = app.test_client()
        self.app.testing = True


    def test_should_be_authenticated(self):
        result = self.app.get("/is-authenticated/", headers={'authorization': self.bearer_header})
        self.assertEquals(result.status_code, 200)


@app.route('/is-authenticated/')
@is_authenticated
def foo():
    return make_response("string", 200)




def create_token(payload):
    token = jwt.encode(payload, 'secret')
    return token