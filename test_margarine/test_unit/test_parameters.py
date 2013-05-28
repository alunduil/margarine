# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import unittest2
import tempfile
import argparse
import sys

try:
    import ConfigParser as configparser
except ImportError:
    import configparser

from margarine.parameters import Parameters
from margarine.parameters import create_argument_parser
from margarine.parameters import create_configuration_parser

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
            ]
    return parameters

class CreateArgumentParserTest(unittest2.TestCase):
    def test_create_argument_parser(self):
        parser = create_argument_parser()

        self.assertIsInstance(parser, argparse.ArgumentParser)

    def test_create_argument_parser_idempotent(self):
        parameters = get_mock_parameters()
        
        parser_a = create_argument_parser(parameters)

        self.assertEqual(parameters, get_mock_parameters())

        parser_b = create_argument_parser(parameters)

        self.assertEqual(str(parser_a), str(parser_b))

    def test_create_argument_parser_properties_default(self):
        parser = create_argument_parser(get_mock_parameters())

        orig = sys.argv
        sys.argv = ["foo"]
        arguments = parser.parse_args()
        sys.argv = orig

        self.assertEqual(arguments.example, "bar")

    def test_create_argument_parser_properties(self):
        parser = create_argument_parser(get_mock_parameters())

        orig = sys.argv
        sys.argv = ["foo", "--example", "foo"]
        arguments = parser.parse_args()
        sys.argv = orig

        self.assertEqual(arguments.example, "foo")

class CreateConfigurationParserTest(unittest2.TestCase):
    def test_create_configuration_parser(self):
        temp = tempfile.NamedTemporaryFile()

        parser = create_configuration_parser(temp.name)

        self.assertIsInstance(parser, configparser.SafeConfigParser)

        temp.close()

    def test_create_argument_parser_idempotent(self):
        parameters = get_mock_parameters()

        temp = tempfile.NamedTemporaryFile()
        
        parser_a = create_configuration_parser(temp.name, parameters)

        self.assertEqual(parameters, get_mock_parameters())

        parser_b = create_configuration_parser(temp.name, parameters)

        self.assertEqual(parser_a.sections(), parser_b.sections())

        temp.close()

    def test_create_configuration_parser_properties_default(self):
        temp = tempfile.NamedTemporaryFile()

        temp.write("[test]\n")

        temp.seek(0)

        parser = create_configuration_parser(temp.name, get_mock_parameters())

        self.assertEqual(parser.get("test", "example"), "bar")

    def test_create_argument_parser_properties(self):
        temp = tempfile.NamedTemporaryFile()

        temp.write("[test]\n")
        temp.write("example = foo\n")

        temp.seek(0)

        parser = create_configuration_parser(temp.name, get_mock_parameters())

        self.assertEqual(parser.get("test", "example"), "foo")

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

