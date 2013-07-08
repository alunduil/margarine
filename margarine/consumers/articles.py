# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging

logger = logging.getLogger(__name__)

def create_article_consumer(channel, method, header, body):
    """Create an article—completing the bottom half of article creation.

    This takes the UUID of the article to create and the URL passed through the
    message queue and fills out the rest of the meta-information as well as
    submitting a job to sanitize the HTML.

    This process should be idempotent and therefore not have any ill-effect if
    invoked multiple times (i.e. POSTed by mutliple users).

    Performs the following specific actions:

    * Updates the etag for the article with a HEAD request.
    * Initializes parsed_at to Null until parsing is complete.

    The following actions should be performed in parallel by a fanout:

    * Submits a reference job to update automatic notations in this and others.
    * Submits the sanitization request for the HTML body. 

    """

    article = json.loads(body)

    logger.debug("article: %s", article)

    articles = get_collection("articles")

    _ = articles.find_one({ "_id": article["_id"] })

    if _ is None: # Article doesn't already have meta-information.
        article["created_at"] = datetime.datetime.now()

     
    
    channel.basic_ack(delivery_tag = method.delivery_tag)

def register(channel):
    """Register the article worker functions on the passed channel.

    Declare exchange, queue, and consumption for the article backend processes.

    Parameters
    ----------

    :channel: The channel to setup the queue over.
    
    """

    # TODO Use a fanout exchange for article creation?
    channel.exchange_declare(exchange = "margarine.articles.topic", type = "topic", auto_delete = True)

    channel.queue_declare(queue = "margarine.articles.create", auto_delete = True)
    channel.queue_bind(queue = "margarine.articles.create", exchange = "margarine.articles.topic", routing_key = "articles.create")

    channel.basic_consume(create_user_consumer, queue = "margarine.articles.create", no_ack = False, consumer_tag = "create")

