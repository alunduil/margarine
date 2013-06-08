# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

"""Provide the blueprint for an articles API for flask.

.. note::

    This blueprint has all methods documented with an assumed prefix.  Thus, 
    the path '/' is in fact something like (defined elsewhere) '/v1/articles/'.

"""

import uuid

from flask import request
from flask import Blueprint

ARTICLE = Blueprint("article", __name__)

@ARTICLE.route('/', methods = [ "POST" ])
def submit_article():
    """Submit a new article for inclusion in margarine.

    Request
    -------

    ::

        POST /
        Content-Type: application/x-www-form-urlencoded

        url=http://blog.alunduil.com/posts/an-explanation-of-lvm-snapshots.html

    ::

        curl -X POST example.com/ -F url="http://blog.alunduil.com/posts/an-explanation-of-lvm-snapshots.html"

    Response
    --------

    ::

        HTTP/1.0 202 Accepted
        Location: /44d85795-248d-5899-b8ca-ac2bd8233755

    """

    # TODO Drop URL in queue for backend processing.

    uuid = uuid.uuid5(uuid.NAMESPACE_URL, request.form["url"])

    response = make_response("", 202)
    response.headers["Location"] = url_for("article", uuid = uuid)

    return response

# TODO Do we need PUT for articles?

@ARTICLE.route('/<uuid>')
def article(uuid):
    """Retrieve a sanitized article.

    Request
    -------

    ::

        GET /44d85795-248d-5899-b8ca-ac2bd8233755
        
    Response
    --------

    ::

        HTTP/1.0 200 Ok

    """

    # TODO Retrieve the document from the datastore
    # TODO Redirect to Cloud Files?

    return

