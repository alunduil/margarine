# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

"""Create the token storage for keeping track of who has a valid token.

Unless we need to worry about being distributed we can get away with a simple
dict as the token store.  Of course, if we do need to be distributed, we should
provide a consistent interface that accesses an external store for the tokens.

"""

from margarine.parameters import Parameters

Parameters("authentication", parameters = [
    { # --authentication-url=TOKEN_STORE_URL; TOKEN_STORE_URL ← "redis://localhost:6739"
        "options": [ "--url" ],
        "metavar": "TOKEN_STORE_URL",
        "default": "redis://localhost:6739",
        "help": "The token storage system to use; defaults: %(default)s.",
        },
    ])

class Tokens(object):
    def __init__(self, token_store_url):
        """Create a connection with the specified token store.

        Using the passed token_store_url we should be able to decompose it into
        the following pieces of information:

        :protocol: Which data store to use.  If this matches the registered
                   name of a backend plugin that backend plugin will be used
                   to provide the interface to the data store.
        :username: The username to login to the data store if required.
        :password: The password to login to the data store if required.
        :hostname: The hostname at which the data store is hosted.
        :port:     The port number at which the data store is hosted.

        The above pieces are put together in typical URL fashion:

        ::

            protocol://username:password@hostname:port

        """

        pass

    def __len__(self):
        pass

    def __getitem__(self, key):
        pass

    def __contains__(self, key):
        return key in self.iterkeys()

    def __iter__(self):
        return self.iterkeys()

    def copy(self):
        # TODO Return a soft-copy.
        pass

    def get(self, key, default = None):
        if key in self:
            return self[key]
        return default

    def has_key(self, key):
        return key in self

    def items(self):
        return list(self.iteritems())

    def iteritems(self):
        pass

    def iterkeys(self):
        pass

    def itervalues(self):
        pass

    def keys(self):
        return list(self.iterkeys())

    def values(self):
        return list(self.itervalues())

def generate_token_store():
    # TODO Get specified configuration file somehow.
    parameters = Parameters("authentication", CONFIGURATION_FILE, PARAMETERS)

    if parameters["debug"] or "token-store-url" not in parameters:
        return {}
    else:
        return Tokens(token_store_url = parameters["token-store-url"])

TOKENS = generate_token_store()

