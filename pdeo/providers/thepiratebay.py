# -*- coding: utf-8 -*-

"""
pdeo.providers.thepiratebay
~~~~~~~~~~~~~~~~~~~~~

This module implements the pdeo thepiratebay.org backend for provider methods.

"""

import requests


class Provider(object):
    def __init__(self):
        pass

    def search(self, title):
        """Search for torrents. Return [{torrent_file, magnet, quality}]."""
        return []
