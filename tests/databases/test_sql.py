#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for pdeo.database.sql"""


import unittest
# import responses

from pdeo.databases import sql


# if version_info[0] == 2:  # utf8 for python2
#     from codecs import open


class PdeoDatabaseSqlTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testEntryPoints(self):
        sql.Database
