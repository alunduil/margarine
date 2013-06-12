# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import pika
import logging

from margarine.parameters import Parameters
from margarine.helpers import URI

logger = logging.getLogger(__name__)

Parameters("communication", parameters = [
    { # --communication-url=URL; URL ← local
        "options": [ "--url" ],
        "default": "amqp://guest:guest@localhost",
        "help": \
                "The URL endpoint of the intra-service communication " \
                "mechanism.  This can be a socket (the default) or an AMQP " \
                "endpoint or anything between that's supported.",
        },
    ])

CONNECTION_BROKER = None

def get_channel():
    """Using the communication.url parameter get a channel for the queue.

    If a connection has already been established we'll simply re-use that
    connection; otherwise, we'll create the connection and return a channel.

    .. note::
        Currently, we only work with an amqp queue and use pika as the
        interaction layer.  If we decide to use other queues we'll have to
        re-evaluate the architecture.

    Returns
    -------

    A channel for queue interaction.

    """

    global CONNECTION_BROKER

    logger.debug("CONNECTION_BROKER: %s", CONNECTION_BROKER)

    if CONNECTION_BROKER is None or not CONNECTION_BROKER.is_open:
        uri = URI(Parameters()["communication.url"])

        credentials = None
        if None not in (uri.username, uri.password):
            credentials = pika.PlainCredentials(uri.username, uri.password)

        # TODO Add SSL support?
        connection_parameters = pika.ConnectionParameters(
                host = uri.host,
                port = uri.port,
                virtual_host = uri.path,
                credentials = credentials
                )

        CONNECTION_BROKER = pika.BlockingConnection(connection_parameters)

    return CONNECTION_BROKER.channel()

