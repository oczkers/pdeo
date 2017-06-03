# -*- coding: utf-8 -*-

"""
pdeo.providers.thepiratebay
~~~~~~~~~~~~~~~~~~~~~

This module implements the pdeo thepiratebay.org backend for provider methods.

"""

import re
from bs4 import BeautifulSoup

from . import BaseProvider


class Provider(BaseProvider):
    def __init__(self, username=None, passwd=None):
        super().__init__()

    def detailsPage(self, url):  # TODO: language
        """Parse details page. Return {imdb, tmdb}."""
        imdb = None
        # TODO: move to BaseProvider
        # TODO?: seach only specific space, not whole page
        # bs = BeautifulSoup(rc, 'html.parser')
        # nfo = bs.find('div', class_='nfo')
        # print(nfo)
        # imdb_id = re.search('(tt[0-9]{4,7})', str(nfo)).group(1)
        rc = self.r.get(url).text
        i = re.search('(tt[0-9]{4,7})', rc)
        if i:
            imdb = i.group(1)  # or None
        else:
            print(url)
        return {'imdb': imdb}

    def search(self, title, year, imdb):  # imdb tmdb
        """Search for torrents. Return [{torrent_file, magnet, quality}]."""
        # TODO: async
        # TODO?: detect codecs
        self.r.cookies.set('lw', 's', domain='thepiratebay.org')  # single view, better for parsing (?)
        category = 207  # hd-movies
        page = 0  # no need to look further
        orderby = 5  # size desc
        url = 'https://thepiratebay.org/search/%s %s/%s/%s/%s' % (title, year, page, orderby, category)
        rc = self.r.get(url).text  # TODO: timeout

        torrents = []
        bs = BeautifulSoup(rc, 'html.parser')  # <3? # TODO: lxml if available
        table = bs.find('table', attrs={'id': 'searchResult'})
        entries = table.findAll('tr', class_=None)
        for i in entries:
            tds = i.find_all('td')
            details_link = 'https://thepiratebay.org/%s' % tds[1].find('a')['href']  # TODO: get imdb/whatever from here to bump score
            name = tds[1].find('a').string
            magnet = tds[3].find('a')['href']
            size = tds[4].string.replace('\xa0', ' ')  # TODO: convert to int # TODO?: fix coding
            seeders = tds[5].string  # int? # TODO?: bump score based on this or maybe lower if not enought
            leechers = tds[6].string  # int?

            details = self.detailsPage(details_link)  # TODO: do this only if we've got imdb to check

            # score  # TODO: move to BaseProvider
            # TODO: score values in config
            score = 0
            score += (0, 10)[tds[3].find('img', alt=re.compile('Trusted')) is not None]
            score += (0, 20)[tds[3].find('img', alt=re.compile('VIP')) is not None]
            score += (0, 50)[tds[3].find('img', alt=re.compile('Moderator')) is not None]
            score += (0, 50)[details['imdb'] == imdb and imdb is not None]  # TODO: same as details

            torrents.append({'name': name,
                             'magnet': magnet,
                             'size': size,
                             'seeders': seeders,
                             'leechers': leechers,
                             'score': score,
                             'imdb': details['imdb']})

        return self._sort(torrents)
