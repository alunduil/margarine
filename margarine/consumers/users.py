# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import hashlib
import logging
import json
import uuid

from margarine.api import information
from margarine.aggregates import get_collection
from margarine.keystores import get_keyspace

logger = logging.getLogger(__name__)

def create_user_consumer(channel, method, header, body):
    """Create a user—completing the bottom half of user creation.

    This takes the meta-information passed through the message queue and
    performs the following operations:

    * Generate User Password
    * Add User to DataStore
    * Email the Password and Verification URL to the User
    * Record the Verification URL in the Token Store

    """
    
    user_information = json.loads(body)

    user_information["hash"] = hashlib.md5("{0}:{1}:{2}".format(user_information["username"], information.AUTHENTICATION_REALM, user_information.pop("password"))).hexdigest()

    logger.debug("hash: %s", user_information["hash"])

    # TODO Save the user in the datastore.

    verification = uuid.uuid4()

    verifications = get_keyspace("verifications")
    verifications.setex(verification, user_information["username"], datetime.timedelta(hours = 6))

    # TODO Email the user the password and verification token.

    channel.basic_ack(delivery_tag = method.delivery_tag)

def register(channel):
    """Register the user worker functions on the passed channel.

    Declare exchange, queue, and consumption for the user backend processes.

    Parameters
    ----------

    :channel: The channel to setup the queue over.
    
    """

    channel.exchange_declare(exchange = "margarine.users.topic", type = "topic", auto_delete = False)

    channel.queue_declare(queue = "margarine.users.create", auto_delete = False)
    channel.queue_bind(queue = "margarine.users.create", exchange = "margarine.users.topic", routing_key = "users.create")

    channel.basic_consume(create_user_consumer, queue = "margarine.users.create", no_ack = False, consumer_tag = "create")

