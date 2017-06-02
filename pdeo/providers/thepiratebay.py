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

    def search(self, title, year):  # imdb tmdb
        """Search for torrents. Return [{torrent_file, magnet, quality}]."""
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

            score = 0
            score += (0, 10)[tds[3].find('img', alt=re.compile('Trusted')) is not None]
            score += (0, 20)[tds[3].find('img', alt=re.compile('VIP')) is not None]
            score += (0, 50)[tds[3].find('img', alt=re.compile('Moderator')) is not None]

            torrents.append({'name': name,
                             'magnet': magnet,
                             'size': size,
                             'seeders': seeders,
                             'leechers': leechers,
                             'score': score})

        return self._sort(torrents)
