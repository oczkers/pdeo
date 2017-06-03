# -*- coding: utf-8 -*-

"""
pdeo.provider
~~~~~~~~~~~~~~~~~~~~~

This module implements the pdeo provider base methods.

"""

import requests
import re


# all provider modules should have:
#   search()  <-- {torrent_file, magnet}

# TODO?: score based on trusted user, seeders, leechers etc.


# chrome 58 @ win10
headers = {  # TODO?: move to config
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

    # TODO?: __get instead of self.r.get

    # search method implemented by specific provider

    def _sort(self, torrents):
        def key(torrents):
            return (torrents['score'],  # sorting by score, size, seeders+leechers
                    torrents['size'],
                    torrents['seeders'] + torrents['leechers'])
        return sorted(torrents, key=key, reverse=True)

    def choose(self, title, year, imdb):
        """Search and choose best torrent."""
        torrents = self.search(title=title, year=year, imdb=imdb)
        if torrents:
            return torrents[0]
        else:
            return None

    def magnetToTorrent(self, magnet):
        """'Converts' magnet to torrent file. This method probably won't work with private trackers."""
        # TODO: validate
        hash = re.search('urn:btih:(.+?)&', magnet).group(1)
        torrent_file = self.r.get('https://itorrents.org/torrent/%s.torrent' % hash).content  # TODO?: don't use the same session
        return torrent_file

    def download(self, url=None, magnet=None):
        """Download torrent file using url or magnetToTorrent."""
        # TODO: validate url download
        # TODO?: Return original torrent file name
        if url:
            return self.r.get(url).content
        else:
            return self.magnetToTorrent(magnet)
