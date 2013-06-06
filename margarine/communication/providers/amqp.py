# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import pika

class AMQPDriver(object):
    def __init__(self, name, queue_url = None):
        self.name = name

        url = urllib.parse(queue_url)

        credentials = pika.PlainCredentials(url.username, url.password)

        connection_parameters = pika.ConnectionParameters(url.hostname, credentials = credentials)

        self.connection_broker = pika.BlockingConnection(connection_parameters)

    def put(self, item, block = True, timeout = None):
        channel = self.connection_broker.channel()

        channel.exchange_declare(exchange = self.name, type = "direct", passive = False, durable = True, auto_delete = False)

        message_properties = pika.BasicProperties()
        message_properties.content_type = "text/plain"

        channel.basic_publish(body = item, exhange = self.name, properties = message_properties, routing_key = "something")

