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
import datetime

from flask import request
from flask import make_response
from flask import abort
from flask import Blueprint
from flask import url_for
from flask.views import MethodView
from flask import render_template

from margarine.blend import information
from margarine.parameters import Parameters
from margarine.communication import get_channel
from margarine.aggregates import get_collection
from margarine.keystores import get_keyspace

logger = logging.getLogger(__name__)

Parameters("api", parameters = [
    { # --api-uuid=UUID; UUID ← uuid.uuid4()
        "options": [ "--uuid" ],
        "default": uuid.uuid4().hex,
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
                "username": request.form.get("username", username),
                "email": request.form.get("email"),
                "name": request.form.get("name"),
                }

        routing_key = "users.create"

        if user is not None:
            routing_key = "users.update"

            message["original_username"] = username

            logger.debug("X-Auth-Token: %s", request.headers.get("X-Auth-Token"))

            if get_keyspace("tokens").get(request.headers.get("X-Auth-Token")) != username:
                # TODO Redirect to token URL?
                raise UnauthorizedError(username = username)

        if message["email"] is None and routing_key == "users.create":
            abort(400)

        message = json.dumps(message)

        channel = get_channel()
        channel.exchange_declare(exchange = "margarine.users.topic", type = "topic", auto_delete = False)
        channel.basic_publish(body = message, exchange = "margarine.users.topic", properties = message_properties, routing_key = routing_key)
        channel.close()

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

        user = get_collection("users").find_one({ "username": username }, { "hash": 0 })

        # TODO Should this be an authenticated action?

        logger.debug("user: %s", user)

        if user is None:
            abort(404)

        # TODO Set JSON mimetype?

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
            # TODO Redirect to token URL?
            raise UnauthorizedError(username = username)

        # TODO Submit queued job and not write from this API?
        get_collection("users").remove({ "username": username })

        return ""

USER.add_url_rule('/<username>', view_func = UserInterface.as_view("users_api"))

class UserPasswordInterface(MethodView):
    """User Password manipulation interface.

    :get:
           * With X-Auth-Token: change password
           * With Verification Token: change password
           * Otherwise: 404
    :post: Submit new password

    """

    def get(self, username):
        """Begin a password change or continue after email verification.

        If an X-Auth-Token header is found, no further validation needs to be
        performed and the password change mechanism is returned.

        If there is no X-Auth-Token header but a query parameter or header with
        an emailed verification code is found (examples shown below), then no
        further validation needs to be performed and the password change
        mechanism is again returned.

        Otherwise, the process is simply initiated and an email is sent with
        a valid URL (including validation token) to continue this process.

        Authenticated Requests
        ----------------------

        ::

            GET /alunduil/password
            X-Auth-Token: 6e585a2d-438d-4a33-856a-8a7c086421ee

        ::

            GET /alunduil/password
            X-Validation-Token: 6e585a2d-438d-4a33-856a-8a7c086421ee

        ::
            
            GET /alunduil/password?verification=6e585a2d-438d-4a33-856a-8a7c086421ee

        Authenticated Response
        ----------------------

        ::

            HTTP/1.0 200 OK

            <!DOCTYPE html>
            <html>
              <body>
                <form name="password" action="/alunduil/password?verification=6e585a2d-438d-4a33-856a-8a7c086421ee" method="post">
                  Password: <input type="password" name="password-0">
                  Password: <input type="password" name="password-1">
                  <input type="submit" value="password-submit">
                </form>
              </body>
            </html>

        Unauthenticated Requests
        ------------------------

        ::

            GET /alunduil/password

        Unauthenticated Response
        ------------------------

        ::

            HTTP/1.0 202 Accepted

        """

        tokens = [ _ for _ in [
            request.headers.get("X-Auth-Token"),
            request.headers.get("X-Verification-Token"),
            request.args.get("verification"),
            ] if _ is not None ]

        logger.debug("len(tokens): %s", len(tokens))

        if len(tokens) > 1:
            abort(400)
        elif len(tokens) == 1:
            verification = tokens[0]

            if get_keyspace("tokens").get(verification) == username:
                get_keyspace("verifications").setex(verification, username, datetime.timedelta(minutes = 3))

            logger.debug("verification token: %s", verification)

            return render_template("password_mechanism.html", username = username, verification = verification)

        message_properties = pika.BasicProperties()
        message_properties.content_type = "application/json"
        message_properties.durable = False

        message = { "username": username, }
        message = json.dumps(message)

        channel = get_channel()
        channel.exchange_declare(exchange = "margarine.users.topic", type = "topic", auto_delete = False)
        channel.basic_publish(body = message, exchange = "margarine.users.topic", properties = message_properties, routing_key = "users.email")
        channel.close()

        return "", 202

    def post(self, username):
        """Update the password for the user and complete the password process.

        Authentication is not handled the same for this method as it is for the
        GET method of the password mechanism.  This method can only be invoked
        properly with the verification query parameter passed from the password
        change mechanism in the GET method.

        Request
        -------

        ::

            POST /alunduil/password?verification=6e585a2d-438d-4a33-856a-8a7c086421ee
            Content-Type: multipart/form-data

            password-0=PASSWORD;password-1=PASSWORD

        Response
        --------

        ::

            HTTP/1.0 202 Accepted

        """

        verification = request.args.get("verification")

        if get_keyspace("verifications").get(verification) != username:
            logger.error("verification token not valid")
            logger.debug("verification: %s", verification)

            abort(400)

        password = request.form.get("password-0")

        if password is None or password != request.form.get("password-1"):
            logger.error("passwords did not match!")

            logger.debug("password-0: %s", password)
            logger.debug("password-1: %s", request.form.get("password-1"))

            abort(400)

        message_properties = pika.BasicProperties()
        message_properties.content_type = "application/json"
        message_properties.durable = False

        message = { 
                "username": username, 
                "password": password,
                }

        message = json.dumps(message)

        channel = get_channel()
        channel.exchange_declare(exchange = "margarine.users.topic", type = "topic", auto_delete = False)
        channel.basic_publish(body = message, exchange = "margarine.users.topic", properties = message_properties, routing_key = "users.password")
        channel.close()

        logger.info("Sent Password Update")

        get_keyspace("verifications").delete(verification)

        return "", 202

USER.add_url_rule('/<username>/password', view_func = UserPasswordInterface.as_view("users_password_api"))
        
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
    
    logger.info("Checking authentication!")

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

    logger.debug("response: %s", request.authorization.response)
    logger.debug("h3: %s", h3)

    if request.authorization.response != h3:
        raise UnauthorizedError(username = username)

    token = uuid.uuid4()

    get_keyspace("tokens").setex(str(token), username, datetime.timedelta(hours = 6))

    return str(token)

