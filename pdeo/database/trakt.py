# -*- coding: utf-8 -*-

"""
pdeo.database.trakt
~~~~~~~~~~~~~~~~~~~~~

This module implements the pdeo trakt.tv backend for database methods.

"""

import requests


client_id = '7b52b4d5eb1105fe4d0e0f479fa00f3d58f671e1e8916bd237ad0a7b3a674a99'
client_secret = '8fdbde42366852783faaf1612509b06d4211a9aff747ba1740056a72be859cf2'


class trakt(object):
    def __init__(self, token=None):
        # TODO?: saving token, token_refresh
        self.r = requests.Session()
        self.token = token
        if not self.token:
            self.authenticate()
        self.r.headers = self.__headers__

    @property
    def __headers__(self):
        return {
            # 'Content-Type': 'application/json',  # requests does this
            'Authorization': 'Bearer %s' % self.token,
            'trakt-api-version': '2',
            'trakt-api-key': client_id
        }

    def authenticate(self):
        """OAuth authentication - first run only."""
        # http://docs.trakt.apiary.io/#reference/authentication-devices/generate-new-device-codes
        data = {'client_id': client_id}  # json.loads?
        rc = self.r.post('https://api.trakt.tv/oauth/device/code', data=data).json()
        # TODO: automatically open browser link
        print('1. Go to the following link: %s' % rc['verification_url'])
        print('2. Enter user code: %s' % rc['user_code'])
        input('done?')  # TODO: async? check instead of asking user

        data = {'code': rc['device_code'],
                'client_id': client_id,
                'client_secret': client_secret}  # json.loads?
        rc = self.r.post('https://api.trakt.tv/oauth/device/token', data=data)
        if rc.status_code == 200:
            rc = rc.json()
            self.token = rc['access_token']
            self.token_refresh = rc['refresh_token']  # needed for refresh without asking user
            # rc['created_at']  # timestamp
            # rc['expires_in']  # 7200 = 3 months?
            return True
        elif rc.status_code == 400:  # waiting for user accept
            pass
        else:
            return False  # TODO?: raise error instead of returing false

        # 404 invalid_code | 409 already used | 410 expired | 418 denied | 429 asking to much, respect interval

    def tokenRefresh(self):
        # token is valid for 3 months
        pass

    def load(self, category='movies'):
        """Loads watchlist."""
        # http://docs.trakt.apiary.io/#reference/sync/get-watchlist
        movies = self.r.get('https://api.trakt.tv/sync/watchlist/%s' % category).json()
        return movies