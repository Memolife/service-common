# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from functools import wraps
import logging
from werkzeug.exceptions import HTTPException
from flask import request, abort, Flask
import jwt

logger = logging.getLogger(__name__)

app = Flask(__name__)

app.config.from_object('config')


def set_request_user():
    # if the user is already set (eg: has_roles or another decorator),
    # we assume it's authenticated
    #
    if hasattr(request, 'user'):
        return

    if request.values.has_key('access_token'):  # Check for token in request params
        token = request.values['access_token']
    else:
        token = request.headers.get('authorization', '').split("Bearer ")[-1]

    if not token:
        abort(401)

    try:
        payload = jwt.decode(token, key=app.config["SECRET_KEY"])
    except jwt.DecodeError:
        abort(401)
    except jwt.ExpiredSignatureError:
        abort(401)

    if payload:
        request.user = payload
        return


def is_authenticated(fn):
    """ Decorator to check request for authorization bearer tokens.
    If token exists and is valid the current user will be set to the
    current request.

    You use it by setting the bearer token in the request authorization header.
    """
    @wraps(fn)
    def wrapped(*args, **kwargs):
        set_request_user()
        return fn(*args, **kwargs)
    return wrapped


def has_roles(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            set_request_user()
            if set(roles).issubset(request.user['roles']):
                return fn(*args, **kwargs)
            abort(401)
        return wrapped
    return decorator


