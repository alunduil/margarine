# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import pika
import logging

from margarine.parameters import Parameters
from margarine.parameters import configure_logging

configure_logging()

from margarine.communication import get_channel
from margarine.consumers import users
from margarine.consumers import articles

logger = logging.getLogger(__name__)

def main():
    """Set us up the bomb.

    Create a consuming process for the various backend processes.

    """

    Parameters().parse()

    # TODO Manage threads for load balancing.

    while True:
        try:
            channel = get_channel()

            users.register(channel)
            articles.register(channel)

            channel.start_consuming()
        except (pika.exceptions.ChannelClosed) as e:
            logger.exception(e)

