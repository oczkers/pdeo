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

    def get(self, title, year, provider=thepiratebay, username=None, passwd=None):  # , quality='hd'
        """Get best torrent. Returns None or {name, magnet, score, size, seeders, leechers}."""  # TODO?: torrent_file
        # TODO: resoltion & bitrate
        # TODO?: convert? magnet to torrent file
        prov = provider.Provider(username=username, passwd=passwd)  # TODO: init provider once, don't relogin on every request
        return prov.choose(title=title, year=year)
