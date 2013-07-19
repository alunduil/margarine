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
import pika
import re

from flask import request
from flask import Blueprint
from flask import abort
from flask import make_response
from flask import url_for
from bson import json_util

from margarine.aggregates import get_collection
from margarine.aggregates import get_container
from margarine.communication import get_channel
from margarine.parameters import Parameters

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

    logger.debug("request.form[url]: '%s'", request.form["url"])
    logger.debug("ASCII: %s", all(ord(c) < 128 for c in request.form["url"]))
    logger.debug("type(request.form[url]): %s", type(request.form["url"]))

    _id = uuid.uuid5(uuid.NAMESPACE_URL, request.form["url"].encode('ascii'))

    logger.debug("type(_id): %s", type(_id.hex))
    logger.debug("_id: %s", _id.hex)

    message_properties = pika.BasicProperties()
    message_properties.content_type = "application/json"
    message_properties.durable = False

    message = {
            "_id": str(_id.hex),
            "url": request.form["url"],
            }

    message = json.dumps(message)

    channel = get_channel()
    channel.exchange_declare(exchange = "margarine.articles.topic", type = "topic", auto_delete = False)
    channel.basic_publish(body = message, exchange = "margarine.articles.topic", properties = message_properties, routing_key = "articles.create")
    channel.close()

    response = make_response("", 202)
    response.headers["Location"] = url_for(".article", article_id = _id)

    return response

Parameters("server", parameters = [
    { # --server-domain=FQDN; FQDN ← HOSTNAME (TLD)
        "options": [ "--domain" ],
        "default": ".".join(socket.gethostname().rsplit('.', 2)[1:]),
        "help": \
                "The base name used in URL generation.  This defaults to the" \
                "host's FQDN.",
        }, # TODO Fix this help message.
    ])

@ARTICLE.route('/<article_id>')
def article(article_id):
    """Retrieve a sanitized article.

    Request
    -------

    ::

        GET /44d85795-248d-5899-b8ca-ac2bd8233755
        
    Response
    --------

    .. note::
        The following is formatted for readability and does not match the 
        actual response from the API.  Also, the body parameter has been
        shortened to fit this example more concisely.

    ::

        HTTP/1.0 200 Ok

        {
          "body": "…Singularity, an Alternative Openstack Guest Agent | Hackery &c…
          "url": "http://blog.alunduil.com/posts/singularity-an-alternative-openstack-guest-agent.html",
          "created_at": {"$date": 1374007667571},
          "etag": "6e2f69536ca15cc18260bffe7583b849",
          "_id": "03db19bb92205b4fb5fc3c4c0e4b1279",
          "parsed_at": {"$date": 1374008521414},
          "size": 9964
        }

    """

    article = get_collection("articles").find_one({ "_id": uuid.UUID(article_id).hex })

    logger.debug("article: %s", article)

    if article is None or "etag" not in article:
        # 404 not only if the object doesn't exist but also if we haven't
        # sanitized the body yet.
        abort(404)

    container_name, object_name = article.pop("text_container_name"), article.pop("text_object_name")

    logger.debug("article: %s", article)

    data = get_container(container_name).get_object(object_name).fetch()

    logger.debug("type(data): %s", type(data))
    logger.debug("len(data): %s", len(data))

    article["body"] = data

    response = make_response(json.dumps(article, default = json_util.default), 200)

    response.headers["Access-Control-Allow-Origin"] = Parameters()["server.domain"]

    return response

