# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

Parameters('keystore', parameters = [
    { # --tokens-url=TOKENS_URL; TOKENS_URL ← "redis://localhost"
        'options': [ '--url' ],
        'metavar': 'TOKENS_URL',
        'default': 'redis://localhost',
        'help': \
                'The URL endpoint for the keystore in which to store ' \
                'tokens.  The default is %(default)s.',
        },
    ])
