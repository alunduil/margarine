# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup

from margarine import information

PARAMS = {}

PARAMS["name"] = information.NAME
PARAMS["version"] = information.VERSION
PARAMS["description"] = information.DESCRIPTION
PARAMS["long_description"] = information.LONG_DESCRIPTION
PARAMS["author"] = information.AUTHOR
PARAMS["author_email"] = information.AUTHOR_EMAIL
PARAMS["url"] = information.URL
PARAMS["license"] = information.LICENSE

PARAMS["classifiers"] = [
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: No Input/Output (Daemon)",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7", # only tested on 2.7
        "Programming Language :: Python :: 2 :: Only", # pika is not 3.* ready
        "Topic :: Education",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ]

PARAMS["keywords"] = [
        "readability",
        "delicious",
        "bookmarks",
        "margins",
        "notes",
        ]

PARAMS["provides"] = [
        "margarine",
        ]

with open('requirements.txt', 'r') as req_fh:
    PARAMS['install_requires'] = req_fh.readlines()

with open('test_margarine/requirements.txt', 'r') as req_fh:
    PARAMS['tests_require'] = req_fh.readlines()

PARAMS['test_suite'] = 'nose.collector'

# TODO Change to entry_points?
PARAMS["scripts"] = [
        "bin/blend",
        "bin/spread",
        "bin/tinge",
        ]

PARAMS["packages"] = [
        "margarine",
        "margarine.blend",
        "margarine.spread",
        "margarine.tinge",
        ]

PARAMS["package_data"] = {
        '': [
            'templates/*.html',
            'static/js/*.js',
            'static/img/*.png',
            'static/css/*.css',
            ],
        }

PARAMS["data_files"] = [
        ("share/doc/{P[name]}-{P[version]}".format(P = PARAMS), [
            "README.rst",
            ]),
        ("share/doc/{P[name]}-{P[version]}/config".format(P = PARAMS), [
            "conf/logging.ini",
            "conf/margarine.ini",
            "conf/pyrax.ini",
            ]),
        ("libexec/{P[name]}".format(P = PARAMS), [
            "conf/blend.wsgi",
            "conf/tinge.wsgi",
            ])
        ]

setup(**PARAMS)
