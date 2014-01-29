# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# =============================================================================
# Monkey Patch as outlined in #23.  TODO Remove this someday…
# -----------------------------------------------------------------------------
import sys
import ConfigParser
import traceback

original_sections = sys.modules['ConfigParser'].ConfigParser.sections

def monkey_sections(self):
    '''Return a list of sections available; DEFAULT is not included in the list.

    Monkey patched to exclude the nosetests section as well.

    '''

    _ = original_sections(self)

    if any([ 'distutils/dist.py' in frame[0] for frame in traceback.extract_stack() ]) and _.count('nosetests'):
        _.remove('nosetests')

    return _

sys.modules['ConfigParser'].ConfigParser.sections = monkey_sections
# -----------------------------------------------------------------------------

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup

from margarine import information

PARAMS = {}

PARAMS['name'] = information.NAME
PARAMS['version'] = information.VERSION
PARAMS['description'] = information.DESCRIPTION
PARAMS['long_description'] = information.LONG_DESCRIPTION
PARAMS['author'] = information.AUTHOR
PARAMS['author_email'] = information.AUTHOR_EMAIL
PARAMS['url'] = information.URL
PARAMS['license'] = information.LICENSE

PARAMS['classifiers'] = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: No Input/Output (Daemon)',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7', # only tested on 2.7
        'Programming Language :: Python :: 2 :: Only', # pika is not 3.* ready
        'Topic :: Education',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        ]

PARAMS['keywords'] = [
        'readability',
        'delicious',
        'bookmarks',
        'margins',
        'notes',
        ]

PARAMS['provides'] = [
        'margarine',
        ]

with open('requirements.txt', 'r') as req_fh:
    PARAMS['install_requires'] = req_fh.readlines()

with open('test_margarine/requirements.txt', 'r') as req_fh:
    PARAMS['tests_require'] = req_fh.readlines()

PARAMS['test_suite'] = 'nose.collector'

PARAMS['scripts'] = [
        'bin/blend',
        'bin/spread',
        'bin/tinge',
        ]

# TODO Change to entry_points?
#PARAMS['entry_points'] = {
#        'console_scripts': [
#            'tinge = margarine.tinge:main',
#            'blend = margarine.blend:main',
#            'spread = margarine.spread:main',
#            ],
#        }

PARAMS['packages'] = [
        'margarine',
        'margarine.blend',
        'margarine.spread',
        'margarine.tinge',
        'margarine.parameters',
        ]

PARAMS['package_data'] = {
        '': [
            'templates/*.html',
            'static/js/*.js',
            'static/img/*.png',
            'static/css/*.css',
            ],
        }

PARAMS['data_files'] = [
        ('share/doc/{P[name]}-{P[version]}'.format(P = PARAMS), [
            'README.rst',
            ]),
        ('share/doc/{P[name]}-{P[version]}/config'.format(P = PARAMS), [
            'config/logging.ini',
            'config/margarine.ini',
            'config/pyrax.ini',
            ]),
        ('libexec/{P[name]}'.format(P = PARAMS), [
            'scripts/blend.wsgi',
            'scripts/tinge.wsgi',
            ])
        ]

setup(**PARAMS)
