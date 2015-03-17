# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from functools import wraps
import logging
import unittest
from flask import Flask, make_response, abort
import jwt
from memolife.auth import is_authenticated, has_roles

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object('config')


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        token = create_token({
            '_id': "testuserid",
            'email': 'test@test.com',
            'roles': ['user', 'admin']
        })
        self.bearer_header = "Bearer {0}".format(token)
        self.app = app.test_client()
        self.app.testing = True

    def test_should_be_authenticated(self):
        result = self.app.get("/is-authenticated/", headers={'authorization': self.bearer_header})
        self.assertEquals(result.status_code, 200)

    def test_should_not_be_authenticated(self):
        result = self.app.get("/is-authenticated/", headers={'authorization': "somerubbish"})
        self.assertEquals(result.status_code, 401)

    def test_should_not_be_authenticated_without_token(self):
        result = self.app.get("/is-authenticated/", headers={})
        self.assertEquals(result.status_code, 401)

    def test_should_only_authenticate_if_admin(self):
        result = self.app.get("/is-admin/", headers={})
        self.assertEquals(result.status_code, 401)

    def test_should_authenticate_when_user_has_admin_role(self):
        result = self.app.get("/is-admin/", headers={'authorization': self.bearer_header})
        self.assertEquals(result.status_code, 200)

    def test_should_authenticate_when_user_has_admin_and_user_role(self):
        result = self.app.get("/is-admin-and-user/", headers={'authorization': self.bearer_header})
        self.assertEquals(result.status_code, 200)

    def test_should_not_authenticate_when_user_has_user_and_admin_but_not_extra_role(self):
        result = self.app.get("/is-user-and-admin-no-extra/", headers={'authorization': self.bearer_header})
        self.assertEquals(result.status_code, 401)


    def test_should_not_authenticate_when_user_is_missing_role(self):
        result = self.app.get("/is-some-role/", headers={'authorization': self.bearer_header})
        self.assertEquals(result.status_code, 401)



@app.route('/is-authenticated/')
@is_authenticated
def foo():
    return make_response("string", 200)


@app.route('/is-admin/')
@has_roles('admin')
def is_admin():
    return make_response("string", 200)


@app.route('/is-admin-and-user/')
@has_roles('admin', 'user')
def is_admin_and_user():
    return make_response("string", 200)

@app.route('/is-user-and-admin-no-extra/')
@has_roles('admin', 'user', 'something')
def extra_role():
    return make_response("string", 200)


@app.route('/is-some-role/')
@has_roles('something')
def is_something_role():
    return make_response("string", 200)


def create_token(payload):
    token = jwt.encode(payload, 'secret')
    return token

if __name__ == '__main__':
    unittest.main()
