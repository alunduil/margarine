# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import uuid

from margarine.parameters import Parameters

Parameters('security', parameters = [
    { # --api-uuid=UUID; UUID ← uuid.uuid4()
        'options': [ '--opaque' ],
        'default': uuid.uuid4().hex,
        'help': \
                'The opaque token used in HTTP digest authentication ' \
                'interactions.  This should be set to a static string ' \
                'unless you run blend on a single server or tie connections ' \
                'to particular servers.  Without this being a static token ' \
                'the authentication mechanism is tied to a particular ' \
                'server.  The default value is a randomly generated UUID4.',
        },
    ])
