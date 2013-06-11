# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import pika
import urllib.parse

from margarine.parameters import Parameters

Parameters("communication", parameters = [
    { # --communication-url=URL; URL ← local
        "options": [ "--url" ],
        "default": "local",
        "help": \
                "The URL endpoint of the intra-service communication " \
                "mechanism.  This can be a socket (the default) or an AMQP " \
                "endpoint or anything between that's supported.",
        },
    ])

CONNECTION_BROKER = None

def get_channel():
    """Using the communication.url parameter get a channel on the queue.

    Returns a channel on the pre-established connection to the queue.

    """

    if CONNECTION_BROKER is None:
        components = urllib.parse.urlparse(Parameters()["communication.url"])

        username, password = components.netloc.split('@', 1)[0].split(':', 1)
        credentials = pika.PlainCredentials(username, password)

        connection_parameters = pika.ConnectionParameters(components.netloc.split('@', 1)[-1], virtual_host = components.path, credentials = credentials)

        CONNECTION_BROKER = pika.BlockingConnection(connection_parameters)

    return CONNECTION_BROKER.channel()

