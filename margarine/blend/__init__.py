# -*- coding: UTF-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import tornado.httpserver
import tornado.web

import margarine.parameters.tornado  # flake8: noqa

from margarine.blend import information
from margarine.blend import articles
from margarine.parameters import PARAMETERS

logger = logging.getLogger(__name__)

PREFIX = r'/{i.API_VERSION}'.format(i = information)

BLEND_APPLICATION = tornado.web.Application(
    [
        ('/'.join([ PREFIX, r'articles', r'([\da-f]{8}-[\da-f]{4}-[\da-f]{4}-[\da-f]{4}-[\da-f]{12})' ]), articles.ArticleReadHandler),
        ('/'.join([ PREFIX, r'articles' ]) + '/', articles.ArticleCreateHandler),
    ]
)


def run():
    PARAMETERS.parse()

    http_server = tornado.httpserver.HTTPServer(BLEND_APPLICATION)

    if PARAMETERS['tornado.debug']:
        http_server.listen(
            port = PARAMETERS['tornado.port'],
            address = PARAMETERS['tornado.address']
        )
    else:
        http_server.bind(
            port = PARAMETERS['tornado.port'],
            address = PARAMETERS['tornado.address']
        )
        http_server.start(0)

    tornado.ioloop.IOLoop.instance().start()
