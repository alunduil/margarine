# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

"""Provide the blueprint for an articles API for flask.

The properties we're starting with are the following:

    * uuid5 (url)
    * url—unique index
    * text → sent to object store upon save (MQ)
    * tags—index
    * notations

      * location
      * note

    * votes—index
    * created_at—index
    * original_etag
    * parsed_at—index
    
    * subscribers—Psuedo parameter, maps to join collection.

      * uuid4—user 
      * uuid5—bookmark
      * subscribed_at

.. note::

    This blueprint has all methods documented with an assumed prefix.  Thus, 
    the path '/' is in fact something like (defined elsewhere) '/v1/articles/'.

"""

import uuid
import json
import logging

from flask import request
from flask import Blueprint
from flask import abort
from flask import make_response

from margarine.aggregates import get_collection

logger = logging.getLogger(__name__)

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

    uuid = uuid.uuid5(uuid.NAMESPACE_URL, request.form["url"])

    message_properties = pika.BasicProperties()
    message_properties.content_type = "application/json"
    message_properties.durable = False

    message = {
            "_id": uuid,
            "url": request.form["url"],
            }

    message = json.dumps(message)

    channel = get_channel()
    channel.exchange_declare(exchange = "margarine.articles.topic", type = "topic", auto_delete = False)
    channel.basic_publish(body = message, exchange = "margarine.articles.topic", properties = message_properties, routing_key = "articles.create")

    response = make_response("", 202)
    response.headers["Location"] = url_for("article", uuid = uuid)

    return response

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
        X-ARTICLE-URL: http://blog.alunduil.com/posts/an-explanation-of-lvm-snapshots.html
        X-ARTICLE-TAGS: [ "lvm", "lvm snapshots", "snapshots", "san", "partitions" ]
        X-ARTICLE-NOTATIONS: [ { "location": null, "note": "lorem ipsum" } ]
        X-ARTICLE-VOTES: 37
        X-ARTICLE-CREATED-AT: 
        X-ARTICLE-ORIGINAL-ETAG: 5d811d796b3e8fefd62233f3772437af
        X-ARTICLE-PARSED-AT:

        <h2>Introduction</h2>
        <p>It seems that disk snapshots have become a hot topic and a confusing
        topic.  I intend to simply outline what snapshots look like in terms of
        the lower layers of abstraction and nothing more.  Snapshots are built 
        into things like LVM, SAN, &amp;c but I will not be covering those 
        technologies.  Instead, what I intend to clarify is how snapshots work 
        in LVM.</p>

        <h2>Lower Layers</h2>
        <h3>Layer 1: The Hard Disk</h3>

    .. note::
        When performing a HEAD operation rather than a GET the body is not
        returned.

    """

    article = get_collection("articles").find_one({ "_id": uuid })

    if article is None:
        abort(404)

    logger.debug("article: %s", article)

    body = article.pop("sanitized_url")

    logger.debug("body: %s", body)

    headers = dict([ ("X-ARTICLE-" + header.replace("_", "-").upper(), value) for header, value in article.iteritems() ])

    logger.debug("headers: %s", headers)

    # TODO Redirect to Cloud Files?

    response = make_response(body, "200")
    response.headers.update(headers)

    logger.debug("response: %s", response)

    return response

