# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

"""All communication mechanisms.

This module includes queue channel acquisition and email handlers.

"""

import pika
import logging
import socket

from margarine.parameters import Parameters
from margarine.helpers import URI

logger = logging.getLogger(__name__)

Parameters("queue", parameters = [
    { # --queue-url=URL; URL ← amqp://guest:guest@localhost
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

Parameters("email", parameters = [
    { # --email-url=URL; URL ← smtp://localhost
        "options": [ "--url" ],
        "default": "smtp://localhost",
        "help": \
                "The URL endpoint of the email relay server used by the " \
                "node.",
        },
    { # --email-from=EMAIL; EMAIL ← noreply@HOSTNAME
        "options": [ "--from" ],
        "default": "noreply@" + socket.gethostname(),
        "help": \
                "The email address used as the FROM address on all " \
                "generated emails.",
        },
    ])

def send_user_email(user, verification):
    """Send an email for user sign up or another action.

    This method encapsulates email handling of the application.  It proxies to
    other methods that correspond to specific actions required for the message
    being handled.

    Parameters
    ----------

    :user:         The user's information to personalize the email.
    :verification: The verification token for verifying a new user.

    This method actually sends the email that is generated and does not return
    anything.

    """

    # TODO i18n this stuff!
    message_text = \
            "Thank you for registering for Margarine.  We hope you enjoy " \
            "the services provided.\n" \
            "\n" \
            "Please, verify your human status by visiting the following " \
            "URL: {verification_url}\n" \
            "\n" \
            "\n" \
            "Thanks,\n" \
            "\n", \
            "Margarine\n"

    message = MIMEText(message_text.format(verification_url = url_for("user.verification", username = user["username"], verification = verification)))

    message["Subject"] = "Margarine Verification"
    message["From"] = "Margarine Verifications <" + Parameters()["email.from"] + ">"
    message["To"] = "{user[name]} <{user[email]}>".format(user = user)
    
    _ = smtplib.SMTP(Parameters()["email.url"])
    _.sendmail(Parameters()["email.from"], [ user["email"] ], message.as_string())
    _.quit()
    
