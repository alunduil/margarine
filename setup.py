# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from distutils.core import setup

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

PARAMS["packages"] = [
        "margarine",
        "margarine.api",
        ]

PARAMS["data_files"] = [
        ("share/doc/{P[name]}-{P[version]}".format(P = PARAMS), [
            "README.md",
            ]),
        ]

setup(**PARAMS)

