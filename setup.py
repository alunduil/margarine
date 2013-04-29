# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from distutils.core import setup

PARAMS = {}

PARAMS["name"] = "margarine"
PARAMS["version"] = "9999"
PARAMS["description"] = \
        "Python application to enhance the web browsing experience and " \
        "display cloud application design."
PARAMS["long_description"] = \
        "A demonstration application that showcases application design for " \
        "cloud deployments.  This application is an amalgamation of the " \
        "functionality found in delicious and readability."
PARAMS["author"] = "Alex Brandt"
PARAMS["author_email"] = "alunduil@alunduil.com"
PARAMS["url"] = "https://github.com/alunduil/margarine"
PARAMS["license"] = "MIT"

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

