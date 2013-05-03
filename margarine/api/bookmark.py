# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import uuid

from flask import request

from margarine.api import information
from margarine.api.application import APPLICATION

@APPLICATION.route('/{i.API_VERSION}/bookmarks/'.format(i = information), methods = [ 'POST' ])
def create_bookmark():
    """Create a new bookmark.

    Request
    -------

    ::

        POST /v1/bookmarks/
        Content-Type: application/x-www-form-urlencoded

        url=http://blog.alunduil.com/posts/an-explanation-of-lvm-snapshots.html

    ::

        curl -X POST example.com/v1/bookmarks/ -F url="http://blog.alunduil.com/posts/an-explanation-of-lvm-snapshots.html"

    Response
    --------

    ::

        HTTP/1.0 202 Accepted
        Location: /v1/bookmarks/44d85795-248d-5899-b8ca-ac2bd8233755
        X-Article-Location: /v1/articles/44d85795-248d-5899-b8ca-ac2bd8233755

    .. note ::
        The short URL for the article is based on the UUID for the bookmark and
        is the first eight bytes of the sha256sum.

    """

    bookmark_uuid = uuid.uuid5(uuid.NAMESPACE_URL, request.form["url"])

    # TODO Drop in queue

    return bookmark_uuid

@APPLICATION.route('/{i.API_VERSION}/bookmarks/<uuid>'.format(i = information), methods = [ 'GET', 'PUT', 'DELETE' ])
def manipulate_bookmark(uuid, property = None):
    """Manipulate a particular bookmark.

    Request
    -------

    Response
    --------

    """

    if request.method == 'GET':
        pass
    elif request.method == 'DELETE':
        pass
    elif request.method == 'PUT':
        pass

@APPLICATION.route('/{i.API_VERSION}/bookmarks/<uuid>/<property>'.format(i = information), methods = [ 'GET', 'PUT', 'DELETE' ])
def manipulate_bookmark_property(uuid, property):
    """Manipulate a particular bookmarks property.

    Request
    -------

    Response
    --------

    """

    if request.method == 'GET':
        pass
    elif request.method == 'DELETE':
        pass
    elif request.method == 'PUT':
        pass

