# -*- coding: UTF-8 -*-
#
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
CONFIGURATION_FILE = os.path.join(CONFIGURATION_DIRECTORY, "margarine.conf")

BASE_PARAMETERS = [
        ]

UNUSED_PARAMETERS = [
        { # --logging_configuration=FILE, -L=FILE; FILE ← CONFIGURATION_DIRECTORY/logging.conf
            "options": [ "--logging_configuration", "-L" ],
            "default": os.path.join(CONFIGURATION_DIRECTORY, "logging.conf"),
            "help": \
                    "The configuration file containing the logging " \
                    "mechanism used by %(prog)s.  Default: %(default)s.",
            },
        ]

def extract_defaults(parameters):
    """Extract the default values for the passed parameters.

    This function will pull the default values from the parameters provided and
    associate them with their names.  Obviously, the returned dict maps the
    parameter's name to its default value(s).

    Arguments
    ---------

    :``parameters``: The parameter definitions (list of dicts) with the form
                     shown in the Examples_ section of Parameters.__init__.

    """

    return dict([ (item["options"][0][2:], item["default"]) for item in parameters if "default" in item ])

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
    logger.debug("parameters: %s", parameters)
    parameters = dict([ (parameter["options"][0][2:], { "args": parameter.pop("options"), "kwargs": parameter }) for parameter in parameters if parameter.get("only") in [ "arguments", None ] ]) # pylint: disable=C0301

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
    
    defaults = extract_defaults(filter(lambda p: p.get("only") in [ "configuration", None ], parameters))

    configuration_parser = ConfigParser.SafeConfigParser(defaults, *args, **kwargs)

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

        self.arguments = create_argument_parser(self.parameters).parse_args()
        self.reinitialize()

    def reinitialize(self):
        """Load the configuration file from disk.

        If a file path is set in this object, we will use it to load a
        configuration parser that we can retrieve keys with.  Otherwise, we
        ignore the configuration file completely.

        """

        if self.file_path is not None:
            logger.debug("file_path: %s", self.file_path)
            self.configuration = create_configuration_parser(self.file_path, self.parameters) # pylint: disable=C0301

    def __len__(self):
        return len(self.parameters)

    def __getitem__(self, key):
        if key not in self:
            raise KeyError(key)

        logger.info("Searching for key: %s", key)

        defaults = extract_defaults(self.parameters)

        value = None

        default = None 
        if key in defaults:
            default = defaults[key]
        logger.debug("default: %s", default)

        value = default

        try:
            if hasattr(self, "configuration") and self.configuration.has_section(self.name):
                value = self.configuration.get(self.name, key)
        except ConfigParser.NoOptionError:
            pass

        logger.debug("value: %s", value)

        if hasattr(self.arguments, key):
            if getattr(self.arguments, key) != default:
                value = getattr(self.arguments, key)

        logger.debug("value: %s", value)

        return value 

    def __contains__(self, key):
        return key in self.iterkeys()

    def __iter__(self):
        return self.iterkeys()

    def copy(self):
        # TODO Think of a way to remove the re-read of files …
        return Paramaters(self.name, self.file_path, self.parameters)

    def get(self, key, default = None):
        if key in self:
            return self[key]
        return default

    def has_key(self, key):
        return key in self

    def items(self):
        return list(self.iteritems())

    def iteritems(self):
        for key in self.iterkeys():
            yield (key, self[key])

    def iterkeys(self):
        for item in self.parameters:
            yield item["options"][0][2:]

    def itervalues(self):
        for key in self.iterkeys():
            yield self[key]

    def keys(self):
        return list(self.iterkeys())

    def values(self):
        return list(self.itervalues())

