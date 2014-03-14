# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import socket

from flask import Flask
from flask import render_template

import margarine.parameters.blend
import margarine.parameters.flask

from margarine.parameters import PARAMETERS

logger = logging.getLogger(__name__)

TINGE = Flask(__name__)

@TINGE.route('/')
def home_page():
    """Return a simple homepage outlining Margarine and allowing signups.

    This is split into two sides:

    * Login and sign-up form on the left
    * Small about and small list of recently added article subjects

    """

    return render_template('index.html', blend_url = PARAMETERS['blend.url'])

@TINGE.route('/article')
def view_article():
    """Return the sanitized view of the article with interface elements.

    The interface elements are a sidebar including the following functions:

    * article star (subscribe)
    * tag cloud (add tags)
    * profile interaction

    If the user isn't logged in they'll see a login form instead of profile
    interaction and will have a grayed out unusable star.

    .. note::
        Should tags be only addable by authenticated users?

    A search box should be shown in the sidebar as well.

    Perhaps the following layout:

    +--------+----------+
    | SEARCH | STAR     |
    +--------+----------+
    | TAG CLOUD         |
    +-------------------+
    | Sign In | Sign Up |
    +-------------------+

    .. note::
        Should the URL schema change to reflect a scheme that will work with
        the pure static page layout (i.e. /article?id=UUID5)?

    Expectations
    ------------

    A query parameter, ``_id``, will be passed with the UUID5 of the article
    to be viewed.

    """

    return render_template('article.index.html', blend_url = Parameters()["api.endpoint"])

logger.debug("error_handlers: %s", TINGE.error_handler_spec)
logger.debug("url map: %s", TINGE.url_map)

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

    flask_parameters["host"] = parameters["flask.host"]
    flask_parameters["port"] = parameters["flask.port"]
    flask_parameters["debug"] = parameters["flask.debug"]

    return flask_parameters

def main():
    PARAMETERS.parse()
    TINGE.run(**_extract_flask_parameters(PARAMETERS))
