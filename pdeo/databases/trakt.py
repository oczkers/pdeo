# -*- coding: utf-8 -*-

"""
pdeo.database.trakt
~~~~~~~~~~~~~~~~~~~~~

This module implements the pdeo trakt.tv backend for database methods.

"""

import requests

from ..config import Config
# from ..exceptions import PdeoError


client_id = '7b52b4d5eb1105fe4d0e0f479fa00f3d58f671e1e8916bd237ad0a7b3a674a99'
client_secret = '8fdbde42366852783faaf1612509b06d4211a9aff747ba1740056a72be859cf2'


# def Show(object):  # TODO?: inhert dict
#     def __init__(self, title, imdb):  # year | trakt, slug, tvdb, tmdb, tvrage
#         self.title = title
#         self.seasons = {}
#
#     def addSeason(self, snumber):
#         self.seasons[snumber] = []
#
#     def addEpisode(self, snumber, enumber):
#         self.seasons[snumber].append(enumber)


class Database(object):
    def __init__(self):
        # TODO?: saving token, token_refresh
        self.config = Config()
        self.r = requests.Session()
        if not self.config.trakt['token']:
            self.__authenticate()
        self.r.headers = self.__headers

    @property
    def __headers(self):
        return {
            # 'Content-Type': 'application/json',  # requests manages this
            'Authorization': 'Bearer %s' % self.config.trakt['token'],
            'trakt-api-version': '2',
            'trakt-api-key': client_id
        }

    def __getToken(self, code):
        """Get token using device_code or refresh_token."""
        data = {'code': code,
                'client_id': client_id,
                'client_secret': client_secret}
        rc = self.r.post('https://api.trakt.tv/oauth/device/token', data=data)
        if rc.status_code == 200:
            rc = rc.json()
            self.config.trakt['token'] = rc['access_token']
            # needed for refresh without asking user
            self.config.trakt['token_refresh'] = rc['refresh_token']
            # self.config['trakt']['token_date'] =
            self.config.save()
            # rc['created_at']  # timestamp
            # rc['expires_in']  # 7200 = 3 months?
            return True
        elif rc.status_code == 400:  # waiting for user accept
            # TODO: sleep, recheck or whatever
            pass
        else:
            # 404 invalid_code | 409 already used | 410 expired | 418 denied | 429 asking to often, respect interval
            return False

    def __authenticate(self):  # shouldn't this be private?
        """OAuth authentication - first run only."""
        # http://docs.trakt.apiary.io/#reference/authentication-devices/generate-new-device-codes
        data = {'client_id': client_id}
        rc = self.r.post('https://api.trakt.tv/oauth/device/code', data=data).json()
        # TODO: automatically open browser link
        print('1. Go to the following link: %s' % rc['verification_url'])
        print('2. Enter user code: %s' % rc['user_code'])
        input('done?')  # TODO: async? check instead of asking user  # TODO: daemon mode without any interupt (error instead)
        self.__getToken(rc['device_code'])  # TODO?: raise error if false

    def __tokenRefresh(self):  # shouldn't this be private?
        # token is valid for 3 months
        self.__getToken(self.token_refresh)  # TODO?: raise error if false

    def loadCollection(self, category='movies'):
        """Loads collection, returns list of movies."""
        rc = self.r.get('https://api.trakt.tv/sync/collection/%s' % category).json()
        return [m[category[:-1]] for m in rc]  # TODO?: parse data (could be usefull to unify with tvshows)

    def load(self, category='movies'):
        """Loads watchlist."""
        # http://docs.trakt.apiary.io/#reference/sync/get-watchlist
        # TODO: tvshows (get imdb/tmdb id from show, nobody cares to attach episode id)
        collection = self.loadCollection(category)
        movies = []
        rc = self.r.get('https://api.trakt.tv/sync/watchlist/%s' % category).json()
        for m in rc:
            if m[m['type']] not in collection:
                movies.append({
                    'date': m['listed_at'],  # TODO: datetime
                    'category': m['type'],
                    'title': m[m['type']]['title'],
                    'year': m[m['type']]['year'],
                    'tmdb': m[m['type']]['ids'].get('tmdb'),
                    'imdb': m[m['type']]['ids'].get('imdb'),
                })
        return movies

    def loadCollectionShows(self):
        """Loads all episodes collection."""
        # TODO: we really need object here, dict/list is just to simple.
        shows = {}
        rc = self.r.get('https://api.trakt.tv/sync/collection/shows').json()
        for show in rc:
            data = {'title': show['show']['title'],
                    'year': show['show']['year'],
                    'trakt': show['show']['ids']['trakt'],  # trakt id
                    'slug': show['show']['ids']['slug'],
                    'tvdb': show['show']['ids']['tvdb'],
                    'imdb': show['show']['ids']['imdb'],
                    'tmdb': show['show']['ids']['tmdb'],
                    'tvrage': show['show']['ids']['tvrage'],
                    'seasons': {}}
            for season in show['seasons']:
                data['seasons'][season['number']] = {}
                data['seasons'][season['number']]['episodes'] = [episode['number'] for episode in season['episodes']]
            shows[data['title']] = data
        return shows

    def loadShows(self):
        """Loads all aired & not watched & not in collection episodes."""
        # TODO: ability to return not aired too (leaks).
        # TODO: drop seasons, use only episodes {title, id, episodes[]}
        collection = self.loadCollectionShows()
        rc = self.r.get('https://api.trakt.tv/users/hidden/progress_watched', params={'type': 'show'}).json()  # TODO?: calendar, progress_collected, recommendations
        hidden = [i['show']['title'] for i in rc]
        shows = {}
        rc = self.r.get('https://api.trakt.tv/sync/watched/shows').json()
        for show in rc:
            if show['show']['title'] in hidden:
                continue
            data = {'title': show['show']['title'],
                    'year': show['show']['year'],
                    'trakt': show['show']['ids']['trakt'],  # trakt id
                    'slug': show['show']['ids']['slug'],
                    'tvdb': show['show']['ids']['tvdb'],
                    'imdb': show['show']['ids']['imdb'],
                    'tmdb': show['show']['ids']['tmdb'],
                    'tvrage': show['show']['ids']['tvrage'],
                    'seasons': {}}
            rc2 = self.r.get('https://api.trakt.tv/shows/%s/progress/watched' % data['slug']).json()  # use trakt instead of slug
            for season in rc2['seasons']:
                data['seasons'][season['number']] = {'episodes': []}
                for episode in season['episodes']:
                    if not episode['completed'] and (data['title'] not in collection or season['number'] not in collection[data['title']]['seasons'] or episode['number'] not in collection[data['title']]['seasons'][season['number']]['episodes']):  # TODO: it might be little bit shorter :-) get('', {})?
                        data['seasons'][season['number']]['episodes'].append(episode['number'])
            shows[data['title']] = data
        return shows

    def clean(self, category='movies'):
        """Remove collected items from watchlist."""
        # TODO: impleent
        pass

    # TODO: def add
