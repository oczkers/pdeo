#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for pdeo.cli"""

import unittest
# import responses

from pdeo import cli


# if version_info[0] == 2:  # utf8 for python2
#     from codecs import open


class PdeoCliTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testEntryPoints(self):
        cli.__main__
