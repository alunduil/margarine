# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

"""URL endpoints and functions related to user management in margarine.

A user in margarine has the following properties:

    * username (from URL)
    * email
    * name (optional)
    * password → md5(username:realm:password)
    * bookmarks
    * tags

Authenticated requests include an ``X-Auth-Token`` header with a token returned
from ``/v1/users/<username>/token``.
    
"""

from flask import request
from flask import abort

from margarine.aggregates.user import User
from margarine.api import information
from margarine.api.application import APPLICATION

@APPLICATION.route('/{i.API_VERSION}/users/<username>'.format(i = information), methods = [ 'GET', 'PUT', 'DELETE' ])
def manipulate_user(username):
    """Manipulate users directly.

    The various user manipulation operations one would expect are exposed
    through this URL endpoint.

    Creating a User
    ---------------

    To create a new user in the system, perform a PUT on the particular user's
    URL that you want created with any parameters (required and optional)
    specified in the form data.

    User Creation Request (New User)
    ''''''''''''''''''''''''''''''''

    ::

        PUT /v1/users/alunduil
        Content-Type: application/x-www-form-urlencoded

        email=alunduil%40alunduil.com

    User Creation Request (Existing User)
    '''''''''''''''''''''''''''''''''''''

    ::

        PUT /v1/users/alunduil
        Content-Type: application/x-www-form-urlencoded
        X-Auth-Token: 6e585a2d-438d-4a33-856a-8a7c086421ee

        email=alunduil%40alunduil.com

    User Creation Response
    ''''''''''''''''''''''

    ::

        HTTP/1.0 202 Accepted

    Once the request for a new user has been accepted (and not rejected), the
    following process occurs:

    #. The user information is verified for correctness
    #. The user information is passed to the message queue
    #. A backend processor pops the user off of the message queue
    #. The backend processor creates the user entry in the database
    #. The backend processor sends an e-mail to the user for verification
    
    The verification e-mail tells the user to visit a link (shown in the
    verification section below) with a particular verification code (secured by
    captcha of some sort).

    Possible Errors
    '''''''''''''''

    :400: Bad Request—A required option was not passed or is improperly
          formatted.
    :401: Unauthorized—An attempt to create an existing user was detected.

    The following are also used when updating a user:

    :409: Conflict—The new username requested is already in use.

    Retrieving a User
    -----------------

    .. note::
        This is an authenticated action that requires an access token from the
        user's token property.

    User Retrieval Request
    ''''''''''''''''''''''

    ::

        GET /v1/users/alunduil
        X-Auth-Token: 6e585a2d-438d-4a33-856a-8a7c086421ee

    User Retrieval Response
    '''''''''''''''''''''''

    ::

        HTTP/1.0 200 OK

        {
          "username": "alunduil",
          "name": "Alex Brandt",
          "email": "alunduil@alunduil.com"
        }

    Possible Errors
    '''''''''''''''

    :401: Unauthorized—Requested a profile that isn't associated with the
          passed token.

    Deleting a User
    ---------------

    .. note::
        This is an authenticated action that requires an access token from the
        user's token property.

    User Deletion Request
    '''''''''''''''''''''

    ::

        DELETE /v1/users/alunduil
        X-Auth-Token: 6e585a2d-438d-4a33-856a-8a7c086421ee

    User Deletion Response
    ''''''''''''''''''''''

    ::

        HTTP/1.0 200 OK

    Possible Errors
    '''''''''''''''

    :401: Unauthorized—Requested a user be deleted that isn't associated with
          the passed token.

    """

    user = None
    users = User.find(username = username)

    if len(users) > 1:
        logger.error("Found duplicate username: %s", username)
        abort(500)
    elif len(users):
        user = users[0]

    if request.method == 'PUT':
        if user is None:
            user = User(username = username, email = request.form["email"])
        else:
            if TOKENS.get(request.headers["X-Auth-Token"]) != username:
                abort(401)

        user.name = request.form.get("name", user.name)

        # TODO Put the password in the verification e-mail?
        if "password" in request.form:
            user.authentication_hash = hashlib.md5("{0}:{1}:{2}".format(username, information.AUTHENTICATION_REALM, request.form["password"])).hexdigest()

        # TODO Drop user.uuid in MQ as a new user function:
        #   * Send verification e-mail.
        
        abort(202)

    elif request.method == 'GET':
        if user is None:
            abort(404)

        return json.dumps(user)

    elif request.method == 'DELETE':
        if user is not None:
            user.delete()

        return ""

@APPLICATION.route('/{i.API_VERSION}/users/<username>/token'.format(i = information))
def get_user_token(username):
    """Get an authorized token for subsequent API calls.

    This is the login method and must be called to get the token required for
    all calls making a note that they require the X-Auth-Token header.

    This call does require a password to be provided (digest authentication is
    used to improve security).

    An authentication challenge has the following form:

    ::

        401 Unauthorized
        Location: /v1/users/${USERNAME}/token
        WWW-Authenticate: Digest realm="margarine.api",
          qop="auth",
          nonce="0cc175b9c0f1b6a831c399e269772661",
          opaque="92eb5ffee6ae2fec3ad71c777531578f"

    This challenge is provided every time the API returns a 401 Unauthorized.
    It is not only presented when requesting this particular URL.

    Request
    -------

    After the above challenge the client should make a request like the
    following to authenticate and receive their token:

    ::
      
        GET /v1/users/alunduil/token HTTP/1.1
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

    Response
    --------

    Once the authentication has been validated in this three step process, the
    application continues and provides the token that was requested.  The token
    is again encrypted (TODO How?) during transit using the exchange that just
    occurred.

    ::

        HTTP/1.1 200 OK

        0b4fb639-edd1-44fe-b757-589a099097a5

    .. note::
        The aforementioned encryption of the token is not currently in effect
        and will be added to this documentation example and implementation
        when it is functional.

    """
    
    if request.authorization.opaque != HOST_UUID.hex:
        abort(401)

    user = None
    users = User.find(username = username)

    if len(users) > 1:
        logger.error("Found duplicate username: %s", username)
        abort(500)
    elif len(users):
        user = users[0]

    ha1 = user.authentication_hash

    ha2 = hashlib.md5("{request.method}:{request.script_path}{request.path}".format(request = request)).hexdigest()

    ha3 = hashlib.md5("{ha1}:{a.nonce}:{a.nc}:{a.cnonce}:{a.qop}:{ha2}".format(ha1 = ha1, a = request.authorization, ha2 = ha2)).hexdigest()

    if request.authorization.response != ha3:
        abort(401)

    token = uuid.uuid4()

    TOKENS[token] = username

    return token

