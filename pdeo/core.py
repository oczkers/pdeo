# -*- coding: utf-8 -*-

"""
pdeo.core
~~~~~~~~~~~~~~~~~~~~~

This module implements the pdeo basic methods.

"""


from .databases import trakt  # TODO: mysql, sqlite
from .providers import thepiratebay


class Core(object):
    def __init__(self, database=trakt):
        self.db = database.Database()

    # TODO: def check multiple

    def check(self, title, provider=thepiratebay, username=None, passwd=None):  # , quality='hd'
        """Check if torrent is available. Return None or {torrent_file, magnet}."""
        # TODO: resoltion & bitrate
        # TODO?: convert? magnet to torrent file
        prov = provider.Provider(username=username, passwd=passwd)  # TODO: init provider once, don't relogin on every request
        return prov.search(title=title)
