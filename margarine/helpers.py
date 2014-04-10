# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import importlib
import itertools
import logging
import os
import re
import sys

logger = logging.getLogger(__name__)


class URI(object):
    '''A URI with accessible components.

    Breaks a URI string (passed into the constructor) into it's components and
    makes those components available as settable properties.

    This URI also has a proper string representation that rebuilds the original
    URI or modified URI.

    Examples
    --------

    >>> str(URI('scheme://username:password@hostname:port/path'))
    'scheme://username:password@hostname:port/path'

    >>> URI('scheme://username:password@hostname:port/path').host
    'hostname'

    '''

    def __init__(self, uri):
        self.uri = uri

        match = re.match(
            r'((?P<scheme>[^:]+)://)?'
            r'((?P<username>[^:]+)(:(?P<password>[^@]+))?@)?'
            r'(?P<host>[^:/]+)?'
            r'(:(?P<port>[^/]+))?'
            r'(?P<path>/[^\?]+)?',
            self.uri
        )

        self.scheme = match.group("scheme")
        self.username = match.group("username")
        self.password = match.group("password")
        self.host = match.group("host")
        self.port = match.group("port")
        self.path = match.group("path")

    def __str__(self):
        _ = ''

        if self.scheme is not None:
            _ += self.scheme + '://'

        if self.username is not None:
            _ += self.username

            if self.password is not None:
                _ += ':' + self.password

            _ += '@'

        if self.host is not None:
            _ += self.host

        if self.port is not None:
            _ += ':' + self.port

        if self.path is not None:
            _ += self.path

        return _


def import_directory(module_basename, directory, update_path = False):
    '''Load all modules in a given directory recursively.

    All python modules in the given directory will be imported.

    Parameters
    ----------

    :``module_basename``: Module name prefix for loaded modules.
    :``directory``:       Directory to recursively load python modules from.
    :``update_path``:     If True, the system path for modules is updated to
                          include ``directory``; otherwise, it is left alone.

    '''

    if update_path:
        update_path = bool(sys.path.count(directory))
        sys.path.append(directory)

    logger.info('loading submodules of %s', module_basename)
    logger.info('loading modules from %s', directory)

    filenames = itertools.chain(*[ [ os.path.join(_[0], filename) for filename in _[2] ] for _ in os.walk(directory) if len(_[2]) ])

    module_names = []
    for filename in filenames:
        if filename.endswith('.py'):
            name = filename

            name = name.replace(directory + '/', '')
            name = name.replace('__init__.py', '')
            name = name.replace('.py', '')
            name = name.replace('/', '.')

            if not len(name):
                continue

            name = module_basename + '.' + name

            known_symbols = set()
            name = '.'.join([ _ for _ in _.split('.') if _ not in known_symbols and not known_symbols.add(_) ])

            if len(_):
                module_names.append(_)

    logger.debug('modules found: %s', list(module_names))

    for module_name in module_names:
        logger.info('loading module %s', module_name)

        try:
            importlib.import_module(module_name)
        except ImportError as e:
            logger.warning('failed loading %s', module_name)
            logger.exception(e)
        else:
            logger.info('successfully loaded %s', module_name)

    if update_path:
        sys.path.remove(directory)
