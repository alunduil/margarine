# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import uuid
import socket

from flask import url_for

from margarine.api.application import APPLICATION
from margarine.information import HOST_UUID

@APPLICATION.errorhandler(401)
def unauthorized(error):
    response = make_response("", 401)

    response.headers["Location"] = url_for('get_user_token')
    response.headers["WWW-Authenticate"] = \
            "Digest realm=\"Margarine API\"," \
            "qop=\"auth\"," \
            "nonce=\"{nonce}\"," \
            "opaque=\"{host_identifier}\""
    repoonse.headers["WWW-Authenticate"].format(
            nonce = uuid.uuid4().hex,
            opaque = HOST_UUID.hex,
            )

    return response

