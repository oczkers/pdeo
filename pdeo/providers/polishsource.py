# -*- coding: utf-8 -*-

"""
pdeo.providers.polishsource
~~~~~~~~~~~~~~~~~~~~~

This module implements the pdeo polishsource.cz provider methods.

"""

import os
import requests

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
        pass
