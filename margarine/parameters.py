# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import os
import sys
import argparse
import copy
import logging
import ConfigParser

from margarine import information

logger = logging.getLogger(__name__)

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

    .. note::
        All other arguments are passed directly to argparse.ArgumentParser.

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

    parameters = copy.deepcopy(parameters)
    parameters = dict([ (item["options"][0][2:], { "args": item.pop("options"), "kwargs": item }) for item in parameters ]) # pylint: disable=C0301
    
    for name, options in parameters.iteritems():
        logger.debug("Adding option, %s, with options, %s and %s", name, options["args"], options["kwargs"]) # pylint: disable=C0301

        parser.add_argument(*options["args"], **options["kwargs"])

    return parser

def create_configuration_parser(file_path, parameters = (), *args, **kwargs):
    """Create a fully initialized configuration parser with the parameters.

    All of the function parameters besides ``parameters`` and ``file_path``
    will be directly passed to ConfigParser.SafeConfigParser.  The returned
    value from this function is the properly prepared SafeConfigParser that
    has already been initialized and loaded.

    Arguments
    ---------

    :``file_path``:  The path to the configuration file to load.
    :``parameters``: The parameter definitions (list of dicts) with the form
                     shown in the Examples_ section of Parameters.__init__.

    .. note::
        All other parameters are passed directly to
        ConfigParser.SafeConfigParser.

    """
    
    defaults = dict([ (item["options"][0][2:], item["default"]) for item in parameters if "default" in item ])

    configuration_parser = ConfigParser.SafeConfigParser(defaults)

    logger.debug("file_path: %s", file_path)

    configuration_parser.read(file_path)

    return configuration_parser

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
        self.parameters = parameters
        self.file_path = file_path

        if not hasattr(self, "arguments"):
            self.arguments = create_argument_parser(self.parameters).parse_args()

        if not hasattr(self, "configuration"):
            self.reinitialize()

    def reinitialize(self):
        if self.file_path is not None:
            logger.debug("file_path: %s", self.file_path)
            self.configuration = create_configuration_parser(self.file_path, self.parameters) # pylint: disable=C0301

    def keys(self):
        pass

    def values(self):
        pass

    def items(self):
        pass

    def has_key(self):
        pass

    def get(self):
        pass

    def clear(self):
        pass

    def setdefault(self):
        pass

    def iterkeys(self):
        pass

    def itervalues(self):
        pass

    def iteritems(self):
        pass

    def pop(self):
        pass

    def popitem(self):
        pass

    def copy(self):
        pass

    def update(self):
        pass

    def __contains__(self):
        return has_key()

    def __iter__(self):
        return iterkeys()

    def __len__(self):
        pass

    def __getitem__(self):
        pass

