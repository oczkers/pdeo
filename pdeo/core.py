# -*- coding: utf-8 -*-

"""
pdeo.core
~~~~~~~~~~~~~~~~~~~~~

This module implements the pdeo basic methods.

"""

import requests

from .database import trakt  # TODO: mysql, sqlite
# from .providers import


class Core(object):
    def __init__(self, database=trakt):
        self.db = database.database()

    def check(self, provider=None, username=None, passwd=None, quality='hd'):
        """Check if torrent is available. Return None or {torrent_file, magnet}."""
        # TODO: resoltion & bitrate
        return None
