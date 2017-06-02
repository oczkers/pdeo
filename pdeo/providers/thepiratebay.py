# -*- coding: utf-8 -*-

"""
pdeo.providers.thepiratebay
~~~~~~~~~~~~~~~~~~~~~

This module implements the pdeo thepiratebay.org backend for provider methods.

"""

import requests

from . import BaseProvider


class Provider(BaseProvider):
    def __init__(self, username=None, passwd=None):
        super().__init__()

    def search(self, title, year):
        """Search for torrents. Return [{torrent_file, magnet, quality}]."""
        # https://thepiratebay.org/s/?q=logan+2017&video=on&category=207&page=0&orderby=99
        params = {'q': '%s+%s' % (title, year),
                  # 'video': 'on',
                  'category': 207,  # hd-movies
                  'page': 0,
                  'orderby': 5}  # size desc
        rc = self.r.get('https://thepiratebay.org', params=params).text  # ssl?
        open('log.log', 'w').write(rc)
        return []
