# -*- coding: utf-8 -*-

"""
pdeo.providers.torrentday
~~~~~~~~~~~~~~~~~~~~~

This module implements the pdeo torrentday.com provider methods.

"""

import requests


class Provider(object):
    def __init__(self):
        pass

    def search(self, title):
        """Search for torrents. Return [{torrent_file, magnet, quality}]."""
        return []
