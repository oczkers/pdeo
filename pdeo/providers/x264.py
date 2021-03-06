# -*- coding: utf-8 -*-

"""
pdeo.providers.x264
~~~~~~~~~~~~~~~~~~~~~

This module implements the pdeo x264.me provider methods.

"""

# import requests

from . import BaseProvider


class Provider(BaseProvider):
    def __init__(self):
        super().__init__()

    def __login(self, username, passwd):
        # Captcha is here, only cookies or rss might work.
        pass

    def search(self, title):
        """Search for torrents. Return [{torrent_file, magnet, quality}]."""
        return []
