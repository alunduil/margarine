# -*- coding: UTF-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import datetime
import json
import logging
import pika
import pytz
import re
import socket
import tornado.web
import uuid

from flask import request
from flask import Blueprint
from flask import abort
from flask import make_response
from flask import url_for
from bson import json_util

import margarine.parameters.tinge

from margarine.aggregates import get_collection
from margarine.aggregates import get_container
from margarine.blend import information
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
    #response.headers["Location"] = url_for(".read_article", article_uuid = _id)
    response.headers["Access-Control-Allow-Origin"] = Parameters()["server.domain"]

    return response


class ArticleReadHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ( 'GET', 'HEAD', 'OPTIONS' )

    def get(self, article_uuid):
        '''Redirect to the requested article data.

        :URL: ``/articles/{ARTICLE_UUID}``

        Parameters
        ----------

        :``ARTICLE_UUID``: UUID of the article being requested.

        Possible Status Codes
        ---------------------

        :301: Permanent redirect to the article's location in an object store.

        Examples
        --------

        1. :request:::
               GET /articles/{ARTICLE_UUID} HTTP/1.0
               [Accept: application/json]

           :response:::
               HTTP/1.0 301 Moved Permanently
               Content-Type: text/html
               Location: {OBJECT_STORE_URL}

               <!DOCTYPE html>
               <html lang="en">
                 <head>
                   <meta charset="utf-8">
                   <title>{UUID}</title>

                   <meta name="author" content="Alex Brandt &gt;alunduil@alunduil.com&lt;">

                   <meta name="viewport" content="width=device-width, initial-scale=1.0">

                   <link href="{OBJECT_STORE_URL}/css/bootstrap.min.css" rel="stylesheet">
                   <link href="{OBJECT_STORE_URL}/css/bootstrap-responsive.min.css" rel="stylesheet" media="screen">
                 </head>
                 <body>
                   <a href="http://{OBJECT_STORE_URL}/articles/{UUID}">{UUID}</a>
                 </body>
               </html>

        '''

        logger.info('STARTING: read article %s', article_uuid)

        cdn_uri = get_container('articles').cdn_uri

        logger.debug('cdn_uri: %s', cdn_uri)

        self.redirect('/'.join([ cdn_uri, 'articles', article_uuid ]), permanent = True)

        logger.info('STOPPING: read article %s', article_uuid)

    head = get
