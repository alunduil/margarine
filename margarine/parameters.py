# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import os
import sys
import argparse

from margarine import information

CONFIGURATION_DIRECTORY = os.path.join(os.path.sep, "etc", "margarine")

def create_argument_parser(parameters = (), *args, **kwargs):
    """Create a fully initialized argument parser with the passed parameters.

    All of the function paramters besides ``parameters`` will be directly
    passed to argparse.ArgumentParser.  The returned value from this function
    is the properly prepared ArgumentParser but the parser has not been run.

    Arguments
    ---------

    :``parameters``: The parameter definitions (list of dicts) with the form
                     shown in the Examples_ section of Parameters.__init__.

    """

    parser = argparse.ArgumentParser(*args, **kwargs)

    version = \
            "%(prog)s-{i.VERSION}\n" \
            "\n" \
            "Copyright {i.COPY_YEAR} by {i.AUTHOR} <{i.AUTHOR_EMAIL}> and " \
            "contributors.  This is free software; see the source for " \
            "copying conditions.  There is NO warranty; not even for " \
            "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE."

    parser.add_argument("--version", action = "version",
            version = version.format(i = information))

class Parameters(object):
    def __init__(self, name = "default", file_path = None, parameters = ()):
        """Turn configuration file path and parameters into a dict-like.

        Construct a Parameters_ container type (dict-like) by using the passed
        ``file_path`` and ``parameters`` to create a hierarchical search for
        configuration items.

        Arguments
        ---------

        :``name``:       The identifying name of this particular Parameters_.
                         The name does not need to be unique but provides a
                         reference to the intent of this particular
                         Parameters_.
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
        >>> Parameters("example", temp.name, [{"options": [ "--example", "-e" ], "default": "foo"}])
        <Parameters[example]: '/tmp/name'>

        """

        self.name = name

        if not hasattr(self, "arguments"):
            self.arguments = create_argument_parser()
            self.arguments.parse_args()

        if not hasattr(self, "configuration"):
            self.reinitialize()

    def keys():
        pass

    def values():
        pass

    def items():
        pass

    def has_key():
        pass

    def get():
        pass

    def clear():
        pass

    def setdefault():
        pass

    def iterkeys():
        pass

    def itervalues():
        pass

    def iteritems():
        pass

    def pop():
        pass

    def popitem():
        pass

    def copy():
        pass

    def update():
        pass

    def __contains__():
        return has_key()

    def __iter__():
        return iterkeys()

    def __len__():
        pass

    def __getitem__():
        pass




