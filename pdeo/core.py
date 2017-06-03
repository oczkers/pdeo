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
        self.db = database.Database()

    # TODO: def check multiple

    def get(self, provider=thepiratebay, username=None, passwd=None):
        """Get best torrent. Returns None or {name, magnet, score, size, seeders, leechers}."""  # TODO?: torrent_file
        # TODO?: initializate provider before calling this?
        # TODO: quality, resoltion & bitrate
        # TODO?: proper convert magnet to torrent file
        # TODO?: ability to search by imdb_id (moviedatabse request first to get metadata) https://www.themoviedb.org/documentation/api
        # TODO?: ability to serach without year (might be necessary for old rips but should we care?)
        movies = self.db.load()
        prov = provider.Provider(username=username, passwd=passwd)
        for movie in movies:
            torrent = prov.choose(title=movie['title'], year=movie['year'], imdb=movie['imdb'])
            if torrent:  # TODO: i don't like this if
                filename = '%s.torrent' % torrent['name']
                open(filename, 'wb').write(torrent['torrent'])  # with?
                print('INFO: torrent downloaded (%s).' % torrent['name'])
            else:
                print('INFO: torrent not found: %s' % movie['title'])  # DEBUG
                pass  # torrent not found
