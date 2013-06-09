# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import unittest2
import tempfile
import argparse
import sys

from margarine.parameters import Parameters

def get_mock_parameters():
    parameters = [
            { # --example=FOO, -e=FOO; FOO ← "bar"
                "options": [ "--example", "-e" ],
                "default": "bar",
                "help": \
                        "Help for the example item.",
                },
            { # --default=DEFAULT, -d=DEFAULT; DEFAULT ← "default"
                "options": [ "--default", "-d" ],
                "default": "default",
                },
            { # --configuration=CONFIGURATION, -c=CONFIGURATION 
                "options": [ "--configuration", "-c" ],
                },
            { # --argument=ARGUMENT, -a=ARGUMENT
                "options": [ "--argument", "-a" ],
                },
            { # --all=ALL, -a=ALL; ALL ← "default"
                "options": [ "--all", "-A" ],
                "default": "default",
                },
            { # --configuration_only=CONFIGURATION, -C=CONFIGURATION
                "options": [ "--configuration_only", "-C" ],
                "only": "configuration",
                },
            { # --argument_only=ARGUMENT, -A=ARGUMENT
                "options": [ "--argument_only", "-O" ],
                "only": "arguments",
                },
            ]
    return parameters

class ParametersConstructionTest(unittest2.TestCase):
    def setUp(self):
        self.parameters = get_mock_parameters()

        self.orig_argv = sys.argv
        sys.argv = [ "foo"]
        
    def tearDown(self):
        sys.argv = self.orig_argv

    def test_construction(self):
        temp = tempfile.NamedTemporaryFile()

        parameters = Parameters("test", temp.name, self.parameters)

        temp.close()

class ParametersRespectsDoubleAsteriskTest(unittest2.TestCase):
    def setUp(self):
        self.temp = tempfile.NamedTemporaryFile()

        self.addCleanup(self.temp.close)

        self.parameters = Parameters("test", self.temp.name, [get_mock_parameters()[0]])

    def test_dict_expansion(self):
        def parameters_to_dict(**kwargs):
            return kwargs

        self.assertEqual(parameters_to_dict(**self.parameters), { "example": "bar" })

class ParametersResolutionTest(unittest2.TestCase):
    def setUp(self):
        self.temp = tempfile.NamedTemporaryFile()

        self.name = "test"
        self.temp.write("[{0}]\n".format(self.name))
        self.temp.write("all           = configuration\n")
        self.temp.write("configuration = configuration\n")
        self.temp.write("example       = configuration\n")

        self.temp.seek(0)

        self.addCleanup(self.temp.close)

        self.orig_argv = sys.argv
        sys.argv = [ "foo", "--argument", "argument", "--all", "argument" ]

        self.parameters = Parameters(self.name, self.temp.name, get_mock_parameters())

    def tearDown(self):
        sys.argv = self.orig_argv

    def test_command_line(self):
        self.assertEqual(self.parameters["argument"], "argument")
        self.assertEqual(self.parameters["all"], "argument")

    def test_configuration_file(self):
        self.assertEqual(self.parameters["configuration"], "configuration")
        self.assertNotEqual(self.parameters["all"], "configuration")

    def test_default(self):
        self.assertEqual(self.parameters["default"], "default")
        self.assertNotEqual(self.parameters["all"], "default")

    def test_override_argument(self):
        self.assertEqual(self.parameters["all"], "argument")

    def test_override_configuration(self):
        self.assertEqual(self.parameters["example"], "configuration")

