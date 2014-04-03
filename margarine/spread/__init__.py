# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import kombu.mixins
import logging
import os

from margarine import helpers
from margarine import queues
from margarine.parameters import PARAMETERS

logger = logging.getLogger(__name__)

CONSUMERS = []


class SpreadWorker(kombu.mixins.ConsumerMixin):
    def __init__(self):
        self.connection = queues.get_connection()

    def get_consumers(self, Consumer, channel):
        helpers.import_directory(__name__, os.path.dirname(__file__))

        return [ Consumer(**kwargs) for kwargs in CONSUMERS ]


def run():
    PARAMETERS.parse()

    try:
        SpreadWorker().run()
    except Exception as error:
        logger.exception(error)
