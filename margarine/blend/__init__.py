# -*- coding: UTF-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import socket

import tornado.web

from flask import Flask
from flask import url_for

from margarine.parameters import Parameters
from margarine.parameters.logging import configure_logging

configure_logging()

from margarine.blend import information
from margarine.blend import articles

from margarine.blend.user import USER
from margarine.blend.user import UnauthorizedError
from margarine.blend.user import http_401_handler

from margarine.blend.articles import ARTICLE
from margarine.blend.tag import TAG

logger = logging.getLogger(__name__)

PREFIX = r'/{i.API_VERSION}'.format(i = information)

BLEND_APPLICATION = tornado.web.Application(
    [
        ('/'.join([ PREFIX, r'articles', r'([\da-f]{8}-[\da-f]{4}-[\da-f]{4}-[\da-f]{4}-[\da-f]{12})' ]), articles.ArticleReadHandler),
    ]
)

def run():
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

BLEND = Flask(__name__)

def _prefix(name):
    """Return the prefix for the API endpoint name given.

    Parameters
    ----------

    :name: The name of the API prefix.

    Returns
    -------

    The true prefix for the API section given the prefix name.

    """

    return "/{i.API_VERSION}/{name}".format(i = information, name = name)

BLEND.register_blueprint(USER, url_prefix = _prefix("users"))
BLEND.register_blueprint(ARTICLE, url_prefix = _prefix("articles"))
BLEND.register_blueprint(TAG, url_prefix = _prefix("tags"))

logger.debug("user resource directory: %s", USER.root_path)
logger.debug("article resource directory: %s", ARTICLE.root_path)
logger.debug("tag resource directory: %s", TAG.root_path)

BLEND.error_handler_spec[None][401] = http_401_handler

logger.debug("error_handlers: %s", BLEND.error_handler_spec)

logger.debug("url map: %s", BLEND.url_map)

def _extract_flask_parameters(parameters):
    """Extract the flask parameters from Parameters.

    This is only necessary to use if translating the stored parameters in a
    Parameters object to parameters to flask.  This does not need to be used
    otherwise and is used internally to start the flask service as part of this
    module.

    Parameters
    ----------

    :parameters: The Parameters object to extract flask parameters from.

    """

    flask_parameters = {}

    logger.debug('parameters: %s', parameters)

    if "flask.host" in parameters:
        flask_parameters["host"] = parameters["flask.host"]

    if "flask.port" in parameters:
        flask_parameters["port"] = int(parameters["flask.port"])

    if "flask.debug" in parameters:
        flask_parameters["debug"] = parameters["flask.debug"]

    return flask_parameters

def main():
    BLEND.run(**_extract_flask_parameters(Parameters().parse()))
