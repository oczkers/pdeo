# -*- coding: utf-8 -*-

"""
pdeo.database
~~~~~~~~~~~~~~~~~~~~~

This module implements the pdeo provider base methods.

"""

import requests

# from . import sql as database
# from . import trakt as database


# all database modules should have:
#   load() <-- loading watchlist, returning {date, category, title, year, tmdb, imdb}


# chrome 58 @ win10
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate,sdch, br',
    'Accept-Language': 'en-US,en;q=0.8',
    # 'Accept-Charset': 'utf-8, iso-8859-1, utf-16, *;q=0.1',
    'Connection': 'keep-alive',
    # 'Keep-Alive': '300',
    'DNT': '1',
}


class BaseProvider(object):
    def __init__(self, username=None, passwd=None):
        self.r = requests.Session()
        self.r.headers = headers
