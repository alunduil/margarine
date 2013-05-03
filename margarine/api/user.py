# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

"""URL endpoints and functions related to user management in margarine.

A user in margarine has the following properties:

    * username (in URL)
    * email
    * name (optional)
    * bio (optional)
    * password (optional)
    * token

Authenticated requests include an ``X-Auth-Token`` header with a token returned
from ``/v1/users/<username>/token``.
    
"""

from flask import request

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

    if request.method == 'PUT':
        pass
    elif request.method == 'GET':
        pass
    elif request.method == 'DELETE':
        pass

@APPLICATION.route('/{i.API_VERSION}/users/<username>/token'.format(i = information))
def get_user_token(username):
    """Get an authorized token for subsequent API calls.

    Request
    -------

    Response
    --------

    """

    pass

@APPLICATION.route('/{i.API_VERSION}/users/<username>/<property>'.format(i = information), methods = [ 'GET', 'PUT', 'DELETE' ])
def manipulate_user_property(username, property):
    """Manipulate particular properties of a user.

    Request
    -------

    Response
    --------

    .. note::
        Not all properties are allowed to be deleted and so some may return a
        405 Method Not Allowed when DELETE is used.

    """

    pass

