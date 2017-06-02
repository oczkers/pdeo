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
        # https://thepiratebay.org/s/?q=logan+2017&video=on&category=207&page=0&orderby=99
        self.r.cookies.set('lw', 's', domain='thepiratebay.org')  # single view, better for parsing (?)
        category = 207  # hd-movies
        page = 0
        orderby = 5  # size desc
        url = 'https://thepiratebay.org/search/%s %s/%s/%s/%s' % (title, year, page, orderby, category)
        rc = self.r.get(url).text  # TODO: timeout
        # rc = rc.replace('\n', '')
        open('log.log', 'w').write(rc)
        # asd = re.search('<td><a href="(/torrent/[0-9]+/.+?)" title="Details for .+?">(.+?)</a></td><td>05-24&nbsp;18:21</td><td><nobr><a href="(magnet.+?)" title="Download this torrent using magnet"><img src="//thepiratebay.org/static/img/icon-magnet.gif" alt="Magnet link" /></a><img src="//thepiratebay.org/static/img/icon_comment.gif" alt="This torrent has [0-9]+ comments." title="This torrent has [0-9]+ comments." /><a href="/user/(.+?)"><img src="//thepiratebay.org/static/img/trusted.png" alt="Trusted" title="Trusted" style="width:11px;" border=\'0\' /></a></nobr></td><td align="right">([0-9\.GiBM]+?)</td><td align="right">([0-9]+)</td><td align="right">([0-9]+)</td>', rc)
        # print(asd.group(1))
        # torrent_link name magnet uploader size seeders leechers

        # This should be in BaseProvider(?)
        torrents = []
        bs = BeautifulSoup(rc, 'html.parser')  # <3? # TODO: lxml if available
        table = bs.find('table', attrs={'id': 'searchResult'})
        entries = table.findAll('tr', class_=None)
        for i in entries:
            tds = i.find_all('td')
            details_link = 'https://thepiratebay.org/%s' % tds[1].find('a')['href']  # TODO: get imdb/whatever from here to bump score
            name = tds[1].find('a').string
            magnet = tds[3].find('a')['href']
            size = tds[4].string  # TODO: convert to int
            seeders = tds[5].string  # int? # TODO?: bump score based on this
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

        return torrents
