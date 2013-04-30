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

        self.parameters = Parameters("test", self.temp.name, get_mock_parameters())

    def test_dict_expansion(self):
        def parameters_to_dict(**kwargs):
            return kwargs

        self.assertEqual(parameters_to_dict(**self.parameters), { "example": "bar" })

class ParametersResolutionTest(unittest2.TestCase):
    def setUp(self):
        self.temp = tempfile.NamedTemporaryFile()
        self.name = "test"

        self.addCleanup(self.temp.close)

        self.parameters = Parameters(self.name, self.temp.name, get_mock_parameters())

    def test_command_line(self):
        self.fail()

    def test_configuration_file(self):
        self.fail()

    def test_default(self):
        self.fail()

