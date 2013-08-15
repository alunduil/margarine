# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import unittest
import tempfile
import sys
import os
import logging

from margarine.parameters import Parameters

logger = logging.getLogger(__name__)

TEST_PARAMETERS = [
        { # --default=DEFAULT, -d=DEFAULT; DEFAULT ← "default"
            "options": [ "--default", "-d" ],
            "default": "default",
            },
        { # --environment=ENV, -e=ENV; ENV ← "environment"
            "options": [ "--environment", "-e" ],
            "default": "default",
            },
        { # --configuration=CONF, -c=CONF; CONF ← "configuration"
            "options": [ "--configuration", "-c" ],
            "default": "default",
            },
        { # --argument=ARG, -a=ARG; ARG ← "argument"
            "options": [ "--argument", "-a" ],
            "default": "default",
            },
        { # --environment_only=ENV, -E=ENV; ENV ← "environment"
            "options": [ "--environment_only", "-E" ],
            "default": "environment",
            "only": "environment",
            },
        { # --configuration-only=CONF, -C=CONF; CONF ← "configuration"
            "options": [ "--configuration-only", "-C" ],
            "default": "configuration",
            "only": "configuration",
            },
        { # --argument-only=ARG, -A=ARG; ARG ← "argument"
            "options": [ "--argument-only", "-A" ],
            "default": "argument",
            "only": "argument",
            },
        ]

class ParametersConstructionTest(unittest.TestCase):
    def setUp(self):
        Parameters._Parameters__shared_state = {}

    def test_zero_parameters_construction(self):
        parameters = Parameters()

        self.assertIsInstance(parameters, Parameters)

    def test_one_parameter_construction(self):
        parameters = Parameters("unused")

        self.assertIsInstance(parameters, Parameters)

    def test_passed_parameters_construction(self):
        parameters = Parameters(parameters = TEST_PARAMETERS)

        self.assertIsInstance(parameters, Parameters)

    def test_passed_file_construction(self):
        fh = tempfile.NamedTemporaryFile()

        parameters = Parameters(file_path = fh.name)

        self.assertIsInstance(parameters, Parameters)

    def test_borg_construction(self):
        p1 = Parameters()
        p2 = Parameters()

        self.assertIs(p1.__dict__, p2.__dict__)

class ParametersRespectsDoubleAsteriskTest(unittest.TestCase):
    def setUp(self):
        Parameters._Parameters__shared_state = {}

        self.parameters = Parameters()

    def test_dict_expansion(self):
        def parameters_to_dict(**kwargs):
            return kwargs

        self.assertEqual(parameters_to_dict(**self.parameters), {})

class ParametersResolutionTest(unittest.TestCase):
    def setUp(self):
        Parameters._Parameters__shared_state = {}

        self.name = "test-section"

        os.environ = {
                "TEST_SCRIPT_TEST_SECTION_ENVIRONMENT": "environment",
                }

        self.temp = tempfile.NamedTemporaryFile(mode = "w")

        self.temp.write("[{0}]\n".format(self.name))
        self.temp.write("configuration = configuration\n")
        self.temp.write("argument      = configuration\n")

        self.temp.seek(0)

        self.addCleanup(self.temp.close)

        self.orig_argv = sys.argv
        sys.argv = [ "test_script", "--test-section-argument=argument" ]

        self.parameters = Parameters(self.name, self.temp.name, TEST_PARAMETERS)
        self.parameters.parse()

    def tearDown(self):
        sys.argv = self.orig_argv

    def test_default(self):
        self.assertEqual(self.parameters["{0}.default".format(self.name)], "default")

    def test_environment(self):
        self.assertEqual(self.parameters["{0}.environment".format(self.name)], "environment")

    def test_configuration(self):
        self.assertEqual(self.parameters["{0}.configuration".format(self.name)], "configuration")

    def test_argument(self):
        self.assertEqual(self.parameters["{0}.argument".format(self.name)], "argument")
