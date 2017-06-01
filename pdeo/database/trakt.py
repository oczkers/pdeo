# -*- coding: utf-8 -*-

"""
pdeo.database.trakt
~~~~~~~~~~~~~~~~~~~~~

This module implements the pdeo trakt.tv backend for database methods.

"""

import requests


client_id = '7b52b4d5eb1105fe4d0e0f479fa00f3d58f671e1e8916bd237ad0a7b3a674a99'

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer [access_token]',
    'trakt-api-version': '2',
    'trakt-api-key': client_id
}


class trakt(object):
    def __init__(self):
        self.r = requests.Session()
        self.r.headers = headers

    def authenticate(self):
        """OAuth authentication - first run only."""
        pass

    def load(self, category='movies'):
        """Loads watchlist."""
        # http://docs.trakt.apiary.io/#reference/sync/get-watchlist
        movies = self.r.get('https://api.trakt.tv/sync/watchlist/%s' % category).json()
        return movies
