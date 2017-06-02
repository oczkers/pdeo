# -*- coding: utf-8 -*-

"""
pdeo.providers.polishsource
~~~~~~~~~~~~~~~~~~~~~

This module implements the pdeo polishsource.cz provider methods.

"""

import requests

from . import BaseProvider


class Provider(BaseProvider):
    def __init__(self):
        super().__init__()

    def search(self, title):
        """Search for torrents. Return [{torrent_file, magnet, quality}]."""
        return []
