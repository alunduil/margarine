# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

"""URL endpoints and functions related to user management in margarine.

The data schema we're starting with is simple and could potentially be moved
to a key-value datastore with pickling as a marshalling technique.

The properties we're starting with are the following:

    * uuid4 (uuid5 username namespace?)
    * username—unique index
    * email
    * name
    * hash → md5(username:realm:password)

    * bookmarks—Psuedo property maps to join collection.

A User in margarine has the following fields:

:_id:      Default MongoDB ID
:username: User's handle
:email:    User's email address
:name:     User's full name
:hash:     User's hash for HTTP Digest ← md5(username:realm:password)

Any request decorated with login_required requires the ``X-Auth-Token`` header
with the value set to a valid token.  This token can be acquired by doing a GET
on /<username>/token.

.. note::
    This blueprint has all methods documented with an assumed prefix.  Thus,
    the path '/' is in fact something like (defined elsewhere) '/v1/users/'.

"""

import uuid
import pika
import json
import logging
import werkzeug.exceptions
import hashlib

from flask import request
from flask import make_response
from flask import abort
from flask import Blueprint
from flask import url_for
from flask.views import MethodView

from margarine.api import information
from margarine.parameters import Parameters
from margarine.communication import get_channel
from margarine.aggregates import get_collection
from margarine.keystores import get_keyspace

logger = logging.getLogger(__name__)

Parameters("api", parameters = [
    { # --api-uuid=UUID; UUID ← uuid.uuid4()
        "options": [ "--uuid" ],
        "default": str(uuid.uuid4()),
        "help": \
                "The UUID used for the HTTP Digest Authentication " \
                "Mechanism.  This should be set to a static string that is " \
                "the same on every deployment but will default to a " \
                "randomly generated UUID4.",
        },
    ])

class UnauthorizedError(werkzeug.exceptions.Unauthorized):
    """Custom unauthorized exception.

    This is identical to the normal werkzeug exception minus one addition.
    This exception also captures the username so it can be used from the error
    handling function as well.

    """

    def __init__(self, description = None, response = None, username = None):
        super(UnauthorizedError, self).__init__(description, response)

        self._username = username

    @property
    def username(self):
        return self._username

def http_401_handler(error):
    """Sends an appropriate 401 Unauthorized page for HTTP Digest.
    
    Working handler for the user login method defined below.  This handler
    does not need to be used but some assumptions about what the handler does
    are made and this handler fits those assumptions.

    """

    logger.debug("type(error): %s", type(error))
    
    logger.debug("error.username: %s", error.username)

    response = make_response("", 401)

    response.headers["Location"] = url_for('user.login', username = error.username)

    authentication_string = \
            "Digest realm=\"{realm}\"," \
            "qop=\"auth\"," \
            "nonce=\"{nonce}\"," \
            "opaque=\"{opaque}\""
    authentication_string = authentication_string.format(
            realm = information.AUTHENTICATION_REALM,
            nonce = uuid.uuid4().hex,
            opaque = Parameters()["api.uuid"],
            )

    logger.debug("authentication_string: %s", authentication_string)

    response.headers["WWW-Authenticate"] = authentication_string

    return response

USER = Blueprint("user", __name__)

class UserInterface(MethodView):
    """User manipulation interface.

    :create: PUT a non-existent username
    :read;   GET an existing username
    :update: PUT an existing username
    :delete: DELETE an existing username

    """

    def put(self, username):
        """Create an User or modify an existing User.

        Create an User
        =============

        To create a new user in the system, perform a PUT on the particular
        user's URL that want created with any parameters (required and
        optional) specified in the form data.

        Request
        -------

        ::
        
            PUT /alunduil
            Content-Type: application/x-www-form-urlencoded

            email=alunduil%40alunduil.com
            name=Alex%20Brandt

        Response
        --------

        ::

            HTTP/1.0 202 Accepted

        Modify an User
        ==============

        This method can also be used to modify an existing user—not just for
        creating new users.

        Request
        -------

        ::

            PUT /alunduil
            Content-Type: application/x-www-form-urlencoded
            X-Auth-Token: 6e585a2d-438d-4a33-856a-8a7c086421ee

            email=alunduil%40alunduil.com

        Response
        --------

        ::

            HTTP/1.0 200 OK

        Possible Errors
        ===============

        :400: Bad Request—A required option was not passed or is improperly
              formatted
        :401: Unauthorized—An attempt to create an existing user was detected

        The following are also used when updating a user:

        :409: Conflict—The new username requested is already in use.

        """

        user = get_collection("users").find_one({ "username": username })
        
        logger.debug("user: %s", user)

        message_properties = pika.BasicProperties()
        message_properties.content_type = "application/json"
        message_properties.durable = False

        message = {
                "username" = request.form.get("username", username),
                "email" = request.form["email"],
                "name" = request.form.get("name"),
                }

        message = json.dumps(message)

        routing_key = "users.create"

        if user is not None:
            routing_key = "users.update"

            if get_keyspace("tokens").get(request.headers.get("X-Auth-Token")) != username:
                raise UnauthorizedError(username = username)

        channel = get_channel()
        channel.exchange_declare(exchange = "margarine.users.topic", type = "topic", auto_delete = False)
        channel.basic_publish(body = message, exchange = "margarine.users.topic", properties = message_properties, routing_key = routing_key)

        return "", 202
    
    def get(self, username):
        """Retrieve an User's information.

        Request
        -------

        ::

            GET /alunduil

        Response
        --------

        ::

            HTTP/1.0 200 OK

            {
              "username": "alunduil",
              "name": "Alex Brandt",
              "email": "alunduil@alunduil.com"
            }

        Possible Errors
        ---------------

        :401: Unauthorized—Requested a profile that isn't associated with the
              passed token.

        """

        user = get_collection("users").find_one({ "username": username })

        # TODO Should this be an authenticated action?

        logger.debug("user: %s", user)

        if user is None:
            abort(404)

        return json.dumps(unicode(user))

    def delete(self, username):
        """Delete an User.

        .. note::
            This is an authenticated action that requires an access token from
            the user's token property.

        Request
        -------

        ::

            DELETE /alunduil
            X-Auth-Token: 6e585a2d-438d-4a33-856a-8a7c086421ee

        Response
        --------

        ::

            HTTP/1.0 200 OK

        Possible Errors
        ---------------

        :401: Unauthorized—Requested a user be deleted that isn't associated
              with the passed token.

        """

        if get_keyspace("tokens").get(request.headers.get("X-Auth-Token")) != username:
            raise UnauthorizedError(username = username)

        users = get_collection("users")

        if users.find_one({ "username": username}).count() > 0:
            users.remove({ "_id": user["_id"] })

        return ""

USER.add_url_rule('/<username>', view_func = UserInterface.as_view("users_api"))

@USER.route('/<username>/token')
def login(username):
    """Get an authorized token for subsequent API calls.

    This is the login method and must be called to get the token required for
    all calls making a note that they require the X-Auth-Token header.

    This call does require a password to be provided (digest authentication is
    used to improve security).  This also means that one cannot simply pass in
    their username and password and get the resulting token.  This token
    request requires two invocations:

    1. Returns the HTTP Digest parameters
    2. Returns the X-Auth-Token value

    Challenge-Response
    ------------------

    A challenge is sent every time the API returns a 401 Unauthoried.  This
    is the first step in getting a token.

    Response (Challenge)
    ''''''''''''''''''''

    ::

        401 Unauthorized
        Location: /alunduil/token
        WWW-Authenticate: Digest realm="margarine.api",
          qop="auth",
          nonce="0cc175b9c0f1b6a831c399e269772661",
          opaque="92eb5ffee6ae2fec3ad71c777531578f"

    Request (Client Authentication Response)
    ''''''''''''''''''''''''''''''''''''''''

    ::
      
        GET /alunduil/token HTTP/1.1
        Host: www.example.com
        Authorization: Digest username="alunduil",
          realm="margarine.api",
          nonce="0cc175b9c0f1b6a831c399e269772661",
          uri="/v1/users/alunduil/token",
          qop=auth,
          nc=00000001,
          cnonce="4a8a08f09d37b73795649038408b5f33",
          response="2370039ff8a9fb83b4293210b5fb53e3",
          opaque="92eb5ffee6ae2fec3ad71c777531578f"

    Response (Token)
    ''''''''''''''''

    ::

        HTTP/1.1 200 OK

        0b4fb639-edd1-44fe-b757-589a099097a5

    """
    
    if request.authorization is None or request.authorization.opaque != Parameters()["api.uuid"]:
        raise UnauthorizedError(username = username)

    user = get_collection("users").find_one({ "username": username })

    logger.debug("user: %s", user)

    if user is None:
        abort(404)

    h1 = user["hash"]

    _ = "{request.method}:{request.path}"
    h2 = hashlib.md5(_.format(request = request)).hexdigest()

    _ = "{h1}:{a.nonce}:{a.nc}:{a.cnonce}:{a.qop}:{h2}"
    h3 = hashlib.md5(_.format(h1 = h1, a = request.authorization, h2 = h2)).hexdigest()

    if request.authorization.response != h3:
        raise UnauthorizedError(username = username)

    token = uuid.uuid4()

    get_keyspace("tokens").setex(token, username, datetime.timedelta(hours = 6))

    return token

@USER.route('/<username>/password')
def password(username):
    """Verify the user and allow a password to be set.

    This verifies the username using the verification token (a randomly
    generated UUID4).  If this token matches what we have in our keystore we
    can provide the mechanism for setting a password for this username.

    If the password is being set this URL will be hit again but rather than a
    GET request (which provides the password change form or mechanism) it will
    be a POST request

    Request
    -------

    ::

        GET /alunduil/e00e587b-0120-4346-98d2-dee86480cce7

    Response
    ------------------

    A challenge is sent every time the API returns a 401 Unauthoried.  This
    is the first step in getting a token.

    Response (Challenge)
    ''''''''''''''''''''

    ::

        401 Unauthorized
        Location: /alunduil/token
        WWW-Authenticate: Digest realm="margarine.api",
          qop="auth",
          nonce="0cc175b9c0f1b6a831c399e269772661",
          opaque="92eb5ffee6ae2fec3ad71c777531578f"

    Request (Client Authentication Response)
    ''''''''''''''''''''''''''''''''''''''''

    ::
      
        GET /alunduil/token HTTP/1.1
        Host: www.example.com
        Authorization: Digest username="alunduil",
          realm="margarine.api",
          nonce="0cc175b9c0f1b6a831c399e269772661",
          uri="/v1/users/alunduil/token",
          qop=auth,
          nc=00000001,
          cnonce="4a8a08f09d37b73795649038408b5f33",
          response="2370039ff8a9fb83b4293210b5fb53e3",
          opaque="92eb5ffee6ae2fec3ad71c777531578f"

    Response (Token)
    ''''''''''''''''

    ::

        HTTP/1.1 200 OK

        0b4fb639-edd1-44fe-b757-589a099097a5

    """
    
    if request.authorization is None or request.authorization.opaque != Parameters()["api.uuid"]:
        raise UnauthorizedError(username = username)

    user = get_collection("users").find_one({ "username": username })

    logger.debug("user: %s", user)

    if user is None:
        abort(404)

    h1 = user["hash"]

    _ = "{request.method}:{request.path}"
    h2 = hashlib.md5(_.format(request = request)).hexdigest()

    _ = "{h1}:{a.nonce}:{a.nc}:{a.cnonce}:{a.qop}:{h2}"
    h3 = hashlib.md5(_.format(h1 = h1, a = request.authorization, h2 = h2)).hexdigest()

    if request.authorization.response != h3:
        raise UnauthorizedError(username = username)

    token = uuid.uuid4()

    get_keyspace("tokens").setex(token, username, datetime.timedelta(hours = 6))

    return token

