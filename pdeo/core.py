# -*- coding: utf-8 -*-

"""
pdeo.core
~~~~~~~~~~~~~~~~~~~~~

This module implements the pdeo basic methods.

"""

import httpx
import re
from blessings import Terminal  # this should be in cli

from .logger import logger
from .config import Config
from .databases import trakt  # TODO: mysql, sqlite
from .providers import thepiratebay, polishsource  # TODO?: vpn/proxy
from .exceptions import PdeoError

colored = Terminal()


class Core(object):
    def __init__(self, database=None, provider=None, debug=False, username=None, passwd=None):
        # TODO?: cache movie details (year at least)
        self.config = Config()  # TODO: config_file
        if database:
            self.config.database = database
        self.db = self._database(self.config.database)
        if provider:
            self.config.provider = provider
        self.provider = self._provider(self.config.provider, username, passwd)

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

    def get(self, destination='.', quality=None, min_size=0):
        """Get best torrent. Returns None or {name, magnet, score, size, seeders, leechers}."""  # TODO?: torrent_file
        # TODO: ability to use other/few providers
        # TODO?: initializate provider before calling this?
        # TODO: quality, resoltion & bitrate
        # TODO?: proper convert magnet to torrent file
        # TODO?: ability to search by imdb_id (moviedatabse request first to get metadata) https://www.themoviedb.org/documentation/api
        # TODO?: ability to serach without year (might be necessary for old rips but should we care?)
        # movies = self.db.load(category='shows')
        if not quality:
            quality = self.config.quality
        movies = self.db.load(category='movies')
        self.logger.debug(f'MOVIES: {movies}')
        for movie in movies:
            if quality != '2160p' and self.uhdPlanned(movie['title'], movie['year']) is True:  # this is ugly
                print(colored.yellow(f'INFO: {movie["title"]} {movie["year"]} UHD is planned, skipping for now.'))
                continue
            torrent = self.provider.search(title=movie['title'], year=movie['year'], imdb=movie['imdb'], quality=quality, min_size=min_size)
            if torrent and torrent['score'] > 0:  # TODO: i don't like this if
                filepath = f'{destination}/{torrent["name"]}.torrent'
                open(filepath, 'wb').write(torrent['torrent'])  # with?
                print(colored.green(f'INFO: {movie["title"]}: {torrent["name"]} {movie["year"]}'))
            else:
                print(colored.red(f'INFO: {movie["title"]} {movie["year"]}'))  # DEBUG
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
                    print(colored.green(f'INFO: {torrent["name"]}.'))
                else:
                    print(colored.red(f'INFO: {episode["title"]}'))  # DEBUG
                    pass  # torrent not found

    def uhdPlanned(self, title, year):
        """Check if 4k is going to be released on bluray."""
        # TODO: validate based on somekind of id (imdb?)
        data = {'section': '4k',  # bluraymovies
                'userid': -1,
                'country': 'US',
                'keyword': title}
        rc = httpx.post('https://www.blu-ray.com/search/quicksearch.php', data=data).text
        # print(rc)  # DEBUG
        if rc != '':
            for i in re.findall(r'&nbsp;(.+?) \(([0-9]{4})\)$', rc, re.MULTILINE):
                print(f'possible uhd found, year not checked yet: {i}')  # DEBUG
                if i[1] == year:
                    return True
        return False


# TODO: logger like in fut
# TODO: imdb_id -> tmdb_id  http://api.themoviedb.org/3/movie/tt0137523?api_key=###
# TODO: filmweb  https://github.com/lopezloo/pyfilmweb
# TODO: upload torrent file via rtorrent api etc.
# TODO: verify year (and get english title?) in tmdb
