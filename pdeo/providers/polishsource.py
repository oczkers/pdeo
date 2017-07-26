# -*- coding: utf-8 -*-

"""
pdeo.providers.polishsource
~~~~~~~~~~~~~~~~~~~~~

This module implements the pdeo polishsource.cz provider methods.

"""

import os
import re
import requests
from bs4 import BeautifulSoup

from . import BaseProvider
from ..exceptions import PdeoError


class Provider(BaseProvider):
    def __init__(self, username, passwd):  # TODO: username & password is not needed when cookies are available
        super().__init__(logger_name=__name__)
        self.login(username, passwd)

    def login(self, username, passwd):
        """Login using saved cookies or username&password."""
        if self.config.polishsource['cookies']:
            self.r.cookies = requests.cookies.cookiejar_from_dict(self.config.polishsource['cookies'])
            rc = self.r.get('https://polishsource.cz').text
        elif not username or passwd:
            raise PdeoError('Username & password or cookies is required for this provider.')  # TODO: PdeoError -> ProviderError
        else:  # TODO: _login
            print('no cookies')
            rc = self.r.get('https://polishsource.cz/login.php').text
            captcha_image = self.r.get('https://polishsource.cz/img.php').content
            open('captcha.jpg', 'wb').write(captcha_image)
            captcha_text = input('Captcha saved as captcha.jpg, please resolve: ')
            os.remove('captcha.jpg')
            data = {'username': username,
                    'password': passwd,
                    'vImageCodP': captcha_text}
            rc = self.r.post('https://polishsource.cz/takelogin.php', data=data).text
        if 'logout.php' in rc:
            self.config.polishsource['cookies'] = self.r.cookies.get_dict()  # this is very simple method, no domain, expire date is saved
            self.config.save()
            return True
        # elif wrongPasswd: login with username
        else:
            open('log.log', 'w').write(rc)  # DEBUG
            # return False
            raise PdeoError('Unknown error when logging to polishsource.cz, please report with logs.')

    def searchAll(self, title, year, imdb, quality, min_size):  # imdb tmdb
        """Search for torrents. Return [{name, magnet, size, seeders, leechers, score, imdb, url}]."""
        # TODO: async
        torrents = []
        params = {'c11': 1,  # category: movies/hd
                  'search': '%s %s %s' % (title, year, quality),
                  'incldead': 1,
                  'scene': 0,
                  'pl': 0,
                  'sub': '',
                  'search_in': 'both'}  # title only?
        rc = self.r.get('https://polishsource.cz/browse.php', params=params).text
        open('pdeo.log', 'w').write(rc)
        if 'Nic nie znaleziono!' in rc:
            return []

        # bs = BeautifulSoup(rc, 'html.parser')  # <3? # TODO: lxml if available
        # table = bs.find('table', attrs={'id': 'restable'})
        # if not table:
        #     return torrents
        # entries = table.findAll('tr')  # broken tags, trs are not closed...
        # for i in entries[1:]:
        for i in rc.split('currentpage')[1].split('<tr')[2:]:
            imdb_id = None
            i = BeautifulSoup(i, 'html.parser')  # <3? # TODO: lxml if available
            tds = i.findAll('td')
            name = tds[1].find('b').string
            if quality not in name:
                continue
            # id = re.match('details.php\?id=([0-9]+)', tds[1].find('a')['href']).group(1)
            id = re.search('id=([0-9]+)', str(tds[1])).group(1)
            size = tds[4].text  # parse
            if size[-2:] == 'GB':
                size = float(size[:-2])
            # TODO: MB
            if size < min_size:
                continue
            # url = 'https://polishsource.cz/' + tds[5].findAll('a')[1]['href']
            seeders = int(tds[6].string)
            leechers = int(tds[7].string)
            if 'Rate IMDB' in tds[1]:  # TODO: optimize
                imdb_id = re.search('(tt[0-9]{4,7})', tds[1].find('a', title='Rate IMDB')['href']).group(1)
            url = 'https://polishsource.cz/downloadssl.php?id=%s&torr=%s' % (id, name + '.torrent')

            score = 0
            score += (0, self.config.score['dead'])[seeders == 0]
            score += seeders  # 50 seeders == imdb, it it good idea?
            score += (0, self.config.score['imdb'])[imdb_id == imdb and imdb is not None]  # TODO: same as details

            torrents.append({'name': name,
                             'magnet': None,
                             'size': size,
                             'seeders': seeders,
                             'leechers': leechers,
                             'score': score,
                             'imdb': imdb_id,
                             'url': url})  # TODO: scheme in BaseProvider
        return torrents
