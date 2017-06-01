#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for pdeo.database"""

# TODO: tests for each backend


import unittest
# import responses

from pdeo import database


# if version_info[0] == 2:  # utf8 for python2
#     from codecs import open


class PdeoDatabaseTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testEntryPoints(self):
        database.database
