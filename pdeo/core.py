# -*- coding: utf-8 -*-

"""
pdeo.core
~~~~~~~~~~~~~~~~~~~~~

This module implements the pdeo basic methods.

"""


from .logger import logger
from .config import Config
from .databases import trakt  # TODO: mysql, sqlite
from .providers import thepiratebay, polishsource  # TODO?: vpn/proxy
from .exceptions import PdeoError


class Core(object):
    def __init__(self, database=None, provider=None, debug=False):
        self.config = Config()  # TODO: config_file
        if database:
            self.config.database = database
        self.db = self._database(self.config.database)
        if provider:
            self.config.provider = provider
        self.provider = self._provider(self.config.provider)

        logger(save=debug)  # init root logger
        self.logger = logger(__name__)

    def _database(self, database):
        """Convert database name to database class."""
        if database == 'trakt':
            database = trakt
        else:
            raise NotImplementedError('Only trakt works for now.')
        return database.Database()

    def _provider(self, provider, username=None, passwd=None):
        """Convert provider name to provider class."""
        if not provider:
            provider = self.provider
        if provider == 'thepiratebay':
            provider = thepiratebay
        elif provider == 'polishsource':
            provider = polishsource
        else:
            raise PdeoError('Unknown provider.')
        return provider.Provider(username=username, passwd=passwd)

    def get(self, destination='.', quality='1080p', min_size=0):
        """Get best torrent. Returns None or {name, magnet, score, size, seeders, leechers}."""  # TODO?: torrent_file
        # TODO: ability to use other/few providers
        # TODO?: initializate provider before calling this?
        # TODO: quality, resoltion & bitrate
        # TODO?: proper convert magnet to torrent file
        # TODO?: ability to search by imdb_id (moviedatabse request first to get metadata) https://www.themoviedb.org/documentation/api
        # TODO?: ability to serach without year (might be necessary for old rips but should we care?)
        movies = self.db.load(category='movies')
        self.logger.debug(f'MOVIES: {movies}')
        for movie in movies:
            torrent = self.provider.search(title=movie['title'], year=movie['year'], imdb=movie['imdb'], quality=quality, min_size=min_size)
            if torrent and torrent['score'] > 0:  # TODO: i don't like this if
                filepath = f'{destination}/{torrent["name"]}.torrent'
                open(filepath, 'wb').write(torrent['torrent'])  # with?
                print(f'INFO: torrent downloaded ({torrent["name"]}).')
            else:
                print(f'INFO: torrent not found: {movie["title"]}')  # DEBUG
                pass  # torrent not found
            # input('next?')  # DEBUG
        # tvshows = self.db.load(category='')

    def getShows(self, destination='.', quality='1080p', min_size=0):
        # TODO: merge into get
        # TODO: optimize somehow to not check every episode
        shows = self.db.loadShows()
        for show in shows.values():
            print(show)
            for episode in show:
                torrent = self.provider.search(title=episode['title'], season=episode['season'], episode=episode['episode'], quality=quality, min_size=min_size)
                if torrent and torrent['score'] > 0:
                    filepath = f'{destination}/{torrent["name"]}.torrent'
                    open(filepath, 'wb').write(torrent['torrent'])  # with?
                    print(f'INFO: torrent downloaded ({torrent["name"]}).')
                else:
                    print(f'INFO: torrent not found: {episode["title"]}')  # DEBUG
                    pass  # torrent not found
                input('next?')  # DEBUG

# TODO: logger like in fut
