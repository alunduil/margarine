# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

"""URL endpoints and functions related to tag management in margarine.

Any request decorated with login_required requires the ``X-Auth-Token`` header
with the value set to a valid token.  This token can be acquired by doing a GET
on /<username>/token.

.. note::
    This blueprint has all methods documented with an assumed prefix.  Thus,
    the path '/' is in fact something like (defined elsewhere) '/v1/users/'.

"""

from flask import Blueprint
from flask.views import MethodView

TAG = Blueprint("tag", __name__)

class TagInterface(MethodView):
    pass

TAG.add_url_rule('/<tag>', view_func = TagInterface.as_view("tags_api"))

