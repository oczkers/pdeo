# -*- coding: utf-8 -*-

"""
pdeo.provider
~~~~~~~~~~~~~~~~~~~~~

This module implements the pdeo provider base methods.

"""

import httpx
import re

from ..config import Config
from ..logger import logger


# all provider modules should have:
#   search()  <-- {torrent_file, magnet}

# TODO?: score based on trusted user, seeders, leechers etc.


# chrome 58 @ win10
headers = {  # TODO?: move to config
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8',
    # 'Accept-Charset': 'utf-8, iso-8859-1, utf-16, *;q=0.1',
    'Connection': 'keep-alive',
    # 'Keep-Alive': '300',
    'DNT': '1',
}


class BaseProvider(object):
    def __init__(self, username=None, passwd=None, logger_name=__name__):  # remove username, passwd?
        # self.logger = logger(child=True)
        self.logger = logger(logger_name)
        self.config = Config()
        self.r = httpx.Client()
        self.r.headers = headers
        self.config.save()

    # TODO?: __get instead of self.r.get
    # TODO: freelech bumps score (+1) on private trackers
    # TODO: norar bumps score +1

    # search method implemented by specific provider

    def __sort(self, torrents):
        """Sort torrents based on score, size, seeders+leechers."""
        # TODO: this is crucial method, allways needs improvement
        def key(torrents):
            return (torrents['score'],
                    torrents['size'],
                    torrents['seeders'] + torrents['leechers'])
        s = sorted(torrents, key=key, reverse=True)
        # s = sorted(torrents, key=lambda k: (k['score'], k['size']), reverse=True)
        print(s)  # DEBUG
        return s

    def magnetToTorrent(self, magnet):
        """'Converts' magnet to torrent file. This method probably won't work with private trackers."""
        # TODO: validate
        hash = re.search('urn:btih:(.+?)&', magnet).group(1)
        torrent_file = self.r.get(f'https://itorrents.org/torrent/{hash}.torrent').content  # TODO?: don't use the same session
        return torrent_file

    def download(self, url=None, magnet=None):
        """Download torrent file using url or magnetToTorrent."""
        # TODO: validate url download
        if url:
            return self.r.get(url).content
        else:
            return self.magnetToTorrent(magnet)

    def search(self, title, season=None, episode=None, year=None, imdb=None, quality=None, min_size=None):
        """Search the one and only torrent. Return torrent file."""
        # TODO?: search(movies=None, shows=None)  movies and shows should be objects/specific dicts
        title = title.replace(':', '').replace(',', '').replace('.', '').replace("'", '')  # TODO?: remove ' and other special signs before searching
        torrents = self.searchAll(title=title, season=season, episode=episode, year=year, imdb=imdb, quality=quality, min_size=min_size)
        if torrents:
            torrent = self.__sort(torrents)[0]
            torrent['torrent'] = self.download(torrent['url'], torrent['magnet'])
            return torrent
        else:
            return None
