# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import unittest2

from margarine.parameters import Parameters

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

class ParametersConstructionTest(unittest2.TestCase):
    def setUp(self):
        self.parameters = get_mock_parameters()

    def test_construction(self):
        parameters = Parameters(self.parameters)

class ParametersRespectsDoubleAsteriskTest(unittest2.TestCase):
    def setUp(self):
        self.parameters = Parameters(self.parameters)

    def test_dict_expansion(self):
        def parameters_to_dict(**kwargs):
            return kwargs

        self.assertEqual(parameters_to_dict(self.parameters), { "example": "bar" })

