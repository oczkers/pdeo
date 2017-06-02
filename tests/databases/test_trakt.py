#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for pdeo.database.trakt"""


import unittest
# import responses

from pdeo.databases import trakt


# if version_info[0] == 2:  # utf8 for python2
#     from codecs import open


class PdeoDatabaseTraktTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testEntryPoints(self):
        trakt.Database
