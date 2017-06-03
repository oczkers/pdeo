# -*- coding: utf-8 -*-

"""
pdeo.core
~~~~~~~~~~~~~~~~~~~~~

This module implements the pdeo basic methods.

"""


from .databases import trakt  # TODO: mysql, sqlite
from .providers import thepiratebay  # TODO?: vpn/proxy


class Core(object):
    def __init__(self, database=trakt):
        # self.db = database.Database()
        pass

    # TODO: def check multiple

    def get(self, title, year, imdb=None, provider=thepiratebay, username=None, passwd=None):  # , quality='hd'
        """Get best torrent. Returns None or {name, magnet, score, size, seeders, leechers}."""  # TODO?: torrent_file
        # TODO: resoltion & bitrate
        # TODO?: ability to search by imdb_id (moviedatabse request first to get metadata)
        # TODO?: ability to serach without year (might be necessary for old rips but should we care?)
        # TODO?: convert? magnet to torrent file
        prov = provider.Provider(username=username, passwd=passwd)  # TODO: init provider once, don't relogin on every request
        return prov.choose(title=title, year=year, imdb=imdb)
