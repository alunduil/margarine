# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import os

CONFIGURATION_DIRECTORY = os.path.join(os.path.sep, "etc", "margarine")

class Parameters(object):
    def __init__(self, file_path = None, parameters = ()):
        """Turn configuration file path and parameters into a dict-like.

        Construct a Parameters_ container type (dict-like) by using the passed
        ``file_path`` and ``parameters`` to create a hierarchical search for
        configuration items.

        Arguments
        ---------

        :``file_path``:  The path to the configuration file this particular set
                         of Parameters_ should refer to when resolving
                         parameters.  If this is ``None``, we will simply skip
                         the configuration resolution completely.
        :``parameters``: The parameter definitions (list of dicts) with the
                         form shown in the Examples_ section below.  These
                         parameters dictate the defaults if nothing comes from
                         the command line or from the configuration file.

        Examples
        --------

        Example ``parameters`` input::

            [
                {
                    "options": [ "--example", "-e" ],
                    "default": "foo",
                    "help":    "The help message!",
                    }
                ]

        >>> import tempfile
        >>> temp = tempfile.NamedTemporaryFile()
        >>> Parameters(temp.name, [{"options": [ "--example" ], "default": "foo"}])
        output

        """

        pass

