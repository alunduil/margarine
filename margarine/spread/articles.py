# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import json
import datetime
import pika
import urllib2
import bs4
import sys
import uuid

from margarine.aggregates import get_collection
from margarine.aggregates import get_container
from margarine.communication import get_channel

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

    .. note::
        The article will need a pre-allocated space in MongoDB for performance
        reasons.  The way we start with the bare necesities and then add
        information at a later time means we may get fragmentation in the data
        stored if we don't pre-allocate enough space.

    """

    article = json.loads(body)

    logger.debug("article: %s", article)

    _id = article.pop("_id")

    articles = get_collection("articles")

    _ = articles.find_one({ "_id": _id })

    logger.debug("Found: %s", _)

    if _ is None or "created_at" not in _:
        article["created_at"] = datetime.datetime.now()

    article = dict([ (k, v) for k, v in article.iteritems() if _ is None or k not in _ or v != _[k] ])

    logger.debug("article: %s", article)
    logger.debug("_id: %s", _id)

    get_collection("articles").update({ "_id": _id }, { "$set": article }, upsert = True)

    message_properties = pika.BasicProperties()
    message_properties.content_type = "application/json"
    message_properties.durable = False

    message = json.dumps({ "_id": _id })

    _ = get_channel()
    _.exchange_declare(exchange = "margarine.articles.create", type = "fanout", auto_delete = False)
    _.basic_publish(body = message, exchange = "margarine.articles.create", properties = message_properties, routing_key = "articles.create")
    _.close()

    channel.basic_ack(delivery_tag = method.delivery_tag)

def update_references_consumer(channel, method, header, body):
    """Update the references to and from the article specified.

    This takes the UUID of the article being added and searches it for links to
    articles (updating the remote references) and then kicks off a temporary
    map reduce process to find other articles that point back at this article
    completing the citation circle.

    This updates two types of notations:

    * citations
    * references

    These are updated on the article in question and the remote article for
    every link found.  This is an extremely heavy process once we have more
    than a trivial amount of articles in the data store.

    .. note::
        This is an easy area for improvement with algorithms on search.

    """

    article = json.loads(body)

    logger.debug("article: %s", article)

    article = get_collection("articles").find_one({ "_id": article["_id"] })

    # TODO Implement the following general algorithm:
    # Retrieve the raw HTML
    # Find all links to other cataloged articles
    # Update those articles with a citation reference to this article
    # Update this article with a reference reference to the remote articles
    # Search all bodies of all articles for links to this article
    # Update those articles with a reference reference to this article
    # Update this article with a citation reference to the remote articles.

    # TODO Automatic indexing of articles:
    #article["tags"] += extract_keywords(soup)

    channel.basic_ack(delivery_tag = method.delivery_tag)

def sanitize_html_consumer(channel, method, header, body):
    """Download and sanitize the HTML for the given article.

    The HTML should be simplified as much as possible without modifying the
    feel of the structure to someone reading the content of the body of the
    document.

    .. note::
        Analysis will be necessary that shows the statistics on sanitized HTML
        size for a determination as to whether we can store it inline in Mongo
        or out of band in an object store like Rackspace Cloud Files.

    The decisions and algorithms used for streamlining the HTML are not
    proprietary in any way and can be used and modified under the terms of this
    file's licensing but more importantly can be improved or modified if 
    imperfections are found.

    """

    _id = json.loads(body)["_id"]

    logger.debug("article._id: %s", _id)

    articles = get_collection("articles")

    article = articles.find_one({ "_id": _id }, { "_id": 0 })

    request = urllib2.Request(article["url"])
    request.get_method = lambda: "HEAD"

    response = urllib2.urlopen(request)

    logger.debug("response: %s", response)
    logger.debug("response.info(): %s", response.info())
    logger.debug("response.info().__class__: %s", response.info().__class__)

    etag = response.info().getheader("etag")

    # TODO Check Last-Modified?
    # TODO Use expires to set the next poll?
    # TODO Respect Cache-Control?
    # TODO Other header considerations.
    # TODO Use Content-Type to set encoding?

    if article.get("etag") != etag:
        logger.info("Parsing full HTML of %s", article["url"])

        article["etag"] = etag

        response = urllib2.urlopen(article["url"])

        soup = bs4.BeautifulSoup(response.read())

        # TODO Use this when more is required:
        #html = sanitize(soup)
        html = soup.get_text()

        article["parsed_at"] = datetime.datetime.now()

        logger.debug("HTML Size: %s B", sys.getsizeof(html))
        article["size"] = sys.getsizeof(html)

        container_part, object_part = str(uuid.UUID(_id)).split("-", 1)

        article["text_container_name"] = "margarine-" + container_part
        article["text_object_name"] = object_part

        logger.info("Uploading text to cloudfiles")

        get_container(article["text_container_name"]).store_object(article["text_object_name"], html, content_type = "text/html")

        logger.info("Uploaded text to cloudfiles")

        articles.update({ "_id": _id }, { "$set": article }, upsert = True)

    logger.info("finished processing article: %s", article["url"])

    channel.basic_ack(delivery_tag = method.delivery_tag)

def register(channel):
    """Register the article worker functions on the passed channel.

    Declare exchange, queue, and consumption for the article backend processes.

    Parameters
    ----------

    :channel: The channel to setup the queue over.
    
    """

    channel.exchange_declare(exchange = "margarine.articles.topic", type = "topic", auto_delete = False)

    channel.queue_declare(queue = "margarine.articles.create", auto_delete = False)
    channel.queue_bind(queue = "margarine.articles.create", exchange = "margarine.articles.topic", routing_key = "articles.create")

    channel.basic_consume(create_article_consumer, queue = "margarine.articles.create", no_ack = False, consumer_tag = "article.create")

    channel.exchange_declare(exchange = "margarine.articles.create", type = "fanout", auto_delete = False)

    channel.queue_declare(queue = "margarine.articles.references", auto_delete = False)
    channel.queue_bind(queue = "margarine.articles.references", exchange = "margarine.articles.create", routing_key = "articles.update")

    channel.basic_consume(update_references_consumer, queue = "margarine.articles.references", no_ack = False, consumer_tag = "article.references")

    channel.queue_declare(queue = "margarine.articles.sanitization", auto_delete = False)
    channel.queue_bind(queue = "margarine.articles.sanitization", exchange = "margarine.articles.create", routing_key = "articles.update")

    channel.basic_consume(sanitize_html_consumer, queue = "margarine.articles.sanitization", no_ack = False, consumer_tag = "article.sanitization")

