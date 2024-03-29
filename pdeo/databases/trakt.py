# -*- coding: utf-8 -*-

"""
pdeo.database.trakt
~~~~~~~~~~~~~~~~~~~~~

This module implements the pdeo trakt.tv backend for database methods.

"""

import httpx

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
        # TODO: remove collected items from watchlist
        self.config = Config()
        self.r = httpx.Client()
        if not self.config.trakt['token']:
            self.__authenticate()
        elif self.config.trakt['token_refresh']:  # use only if necessary (token_date)
            self.__getToken(refresh_token=self.config.trakt['token_refresh'])
        self.r.headers = self.__headers

    @property
    def __headers(self):
        return {
            # 'Content-Type': 'application/json',  # requests manages this
            'Authorization': f'Bearer {self.config.trakt["token"]}',
            'trakt-api-version': '2',
            'trakt-api-key': client_id
        }

    def __getToken(self, code=None, refresh_token=None):
        """Get token using device_code or refresh_token."""
        data = {'client_id': client_id,
                'client_secret': client_secret}
        if code:
            data['code'] = code
            data['grant_type'] = 'authorization_code'
            url = 'https://api.trakt.tv/oauth/device/token'
        elif refresh_token:
            data['refresh_token'] = refresh_token
            data['grant_type'] = 'refresh_token'
            url = 'https://api.trakt.tv/oauth/token'
        rc = self.r.post(url, data=data)
        if rc.status_code == 200:
            rc = rc.json()
            print(rc)
            self.config.trakt['token'] = rc['access_token']
            # needed for refresh without asking user
            self.config.trakt['token_refresh'] = rc['refresh_token']
            # self.config['trakt']['token_date'] =
            self.config.save()
            # rc['created_at']  # timestamp
            # rc['expires_in']  # 7200 = 3 months?
            return True
        elif rc.status_code == 400:  # waiting for user accept OR ERROR
            # TODO: sleep, recheck or whatever
            rc = rc.json()
            if rc['error'] == 'invalid_grant' and rc['error_description'] == 'The provided authorization grant is invalid, expired, revoked, does not match the redirection URI used in the authorization request, or was issued to another client.':
                print('TRAKT: all tokens probably expired, refreshing')
                self.__authenticate()
                return True
            pass
        else:
            # 404 invalid_code | 409 already used | 410 expired | 418 denied | 429 asking to often, respect interval
            print(rc.status_code)
            print(rc.text)
            return False

    def __authenticate(self):  # shouldn't this be private?
        """OAuth authentication - first run only."""
        # http://docs.trakt.apiary.io/#reference/authentication-devices/generate-new-device-codes
        data = {'client_id': client_id}
        rc = self.r.post('https://api.trakt.tv/oauth/device/code', data=data).json()
        # TODO: automatically open browser link
        print(f'1. Go to the following link: {rc["verification_url"]}')
        print(f'2. Enter user code: {rc["user_code"]}')
        input('done?')  # TODO: async? check instead of asking user  # TODO: daemon mode without any interupt (error instead)
        self.__getToken(rc['device_code'])  # TODO?: raise error if false

    def __tokenRefresh(self):  # shouldn't this be private?
        # token is valid for 3 months
        self.__getToken(self.token_refresh)  # TODO?: raise error if false

    def omdb(self, title=None, imdb_id=None):  # MOVE TO SEPARATE MODULE
        params = {'apikey': self.config.omdb_key}
        if title:
            params['t'] = title
        elif imdb_id:
            params['i'] = imdb_id
        rc = self.r.get('http://omdbapi.com', params=params).json()
        print(rc)
        return rc

    def loadCollection(self, category='movies'):
        """Loads collection, returns list of movies."""
        rc = self.r.get(f'https://api.trakt.tv/sync/collection/{category}')
        print(rc.status_code)
        print(rc.content)
        rc = rc.json()
        if category == 'movies':
            items = [i[category[:-1]] for i in rc]
        elif category == 'shows':
            items = []
            for i in rc:
                item = i[category[:-1]]
                for s in i['seasons']:
                    for e in s['episodes']:
                        item['season'] = s['number']
                        item['number'] = e['number']
                        # del item['year']  # there is no year in watchlist episode object, we have to keep compatibility
                        items.append(item)
        else:
            adsasdasd_unknown_category
            # raise
        print(items)  # DEBUG
        return items  # TODO?: parse data (could be usefull to unify with tvshows)

    def load(self, category='movies'):
        """Loads watchlist."""
        # http://docs.trakt.apiary.io/#reference/sync/get-watchlist
        # TODO: tvshows (get imdb/tmdb id from show, nobody cares to attach episode id)
        # TODO?: dont parse just attach 'type' object (with corrected ids and year for shows)
        collection = self.loadCollection(category)
        items = []
        if category == 'shows':  # separate request for shows, seasons, episodes...
            category = 'episodes'
        rc = self.r.get(f'https://api.trakt.tv/sync/watchlist/{category}').json()
        print(rc)
        # addas
        for i in rc:
            if i[i['type']] not in collection:
                if i[i['type']]['ids']['imdb']:
                    year = self.omdb(imdb_id=i[i['type']]['ids']['imdb']).get('Year', i[i['type']].get('year'))  # shows
                else:  # by title only
                    year = self.omdb(title=i[i['type']]['title']).get('Year', i[i['type']].get('year'))  # shows
                items.append({
                    'date': i['listed_at'],  # TODO: datetime
                    'category': i['type'],
                    'title': i[i['type']]['title'],
                    # 'year': i[i['type']].get('year') or i['show']['year'],  # TODO?: show.year in get instead of or?
                    'year': year or i.get('show', {}).get('year'),  # TODO?: show.year in get instead of or?
                    'tmdb': i[i['type']]['ids'].get('tmdb'),
                    'imdb': i[i['type']]['ids'].get('imdb'),
                })
        return items

    def loadCollectionShows(self):
        """Loads all episodes collection."""
        # TODO: we really need object here, dict/list is just to simple.
        shows = {}
        rc = self.r.get('https://api.trakt.tv/sync/collection/shows').json()
        for show in rc:
            episodes = []
            for season in show['seasons']:
                for episode in season['episodes']:
                    data = {'title': show['show']['title'],
                            'year': show['show']['year'],
                            'trakt': show['show']['ids']['trakt'],  # trakt id
                            'slug': show['show']['ids']['slug'],
                            'tvdb': show['show']['ids']['tvdb'],
                            'imdb': show['show']['ids']['imdb'],
                            'tmdb': show['show']['ids']['tmdb'],
                            'tvrage': show['show']['ids']['tvrage'],
                            'season': season['number'],
                            'episode': episode['number']}
                    episodes.append(data)
            shows[data['title']] = episodes
        return shows

    def loadAllShows(self):
        """Loads all aired & not watched & not in collection episodes."""
        # TODO: ability to return not aired too (leaks).
        # TODO: drop seasons, use only episodes {title, id, episodes[]}
        # TODO: add watchlist, not being in progress
        # TODO: optional in progress, not in watchlist (below code)
        collection = self.loadCollectionShows()
        rc = self.r.get('https://api.trakt.tv/users/hidden/progress_watched', params={'type': 'show'}).json()  # TODO?: calendar, progress_collected, recommendations
        hidden = [i['show']['title'] for i in rc]
        shows = {}
        rc = self.r.get('https://api.trakt.tv/sync/watched/shows').json()
        for show in rc:
            episodes = []
            if show['show']['title'] in hidden:
                continue
            rc2 = self.r.get(f'https://api.trakt.tv/shows/{show["show"]["ids"]["slug"]}/progress/watched').json()  # use trakt id instead of slug
            for season in rc2['seasons']:
                for episode in season['episodes']:
                    data = {'title': show['show']['title'],
                            'year': show['show']['year'],
                            'trakt': show['show']['ids']['trakt'],  # trakt id
                            'slug': show['show']['ids']['slug'],
                            'tvdb': show['show']['ids']['tvdb'],
                            'imdb': show['show']['ids']['imdb'],
                            'tmdb': show['show']['ids']['tmdb'],
                            'tvrage': show['show']['ids']['tvrage'],
                            'season': season['number'],
                            'episode': episode['number']}
                    if not episode['completed'] and data not in collection.get(data['title'], ()):
                        episodes.append(data)
            if len(episodes) > 0:
                shows[data['title']] = episodes
        return shows

    def clean(self, category='movies'):
        """Remove collected items from watchlist."""
        # TODO: impleent
        pass

    # TODO: def add
