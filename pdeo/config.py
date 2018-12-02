# -*- coding: utf-8 -*-

"""
pdeo.config
~~~~~~~~~~~~~~~~~~~~~

This module implements the pdeo config methods.

"""

import yaml
from os.path import expanduser

from .exceptions import PdeoError


class Config(object):
    def __init__(self, filename='pdeo.yml', path=None):  # default filename
        # TODO: config in home
        if not path:
            path = expanduser('~/.config/')
        self.config_file = path + filename
        self._load()

    def _load(self):
        try:
            config = yaml.safe_load(open(self.config_file, 'r'))
        except IOError as e:  # FileNotFoundError doesn't exists in python2 AND pypy3
            print(e)  # config does not exists, load default
            config = {}
        except yaml.YAMLError as e:
            print(e)  # config cannot be loaded
            raise PdeoError('Config cannot be loaded, probably broken.')

        self.destination = config.get('destination', '.')
        self.quality = config.get('quality', '1080p')
        self.min_size = config.get('min_size', 5)
        self.score = config.get('score', {'dead': -20,
                                          'trusted': 10,
                                          'vip': 20,
                                          'moderator': 50,
                                          'imdb': 50,
                                          'custom': {}})  # TODO: custom score ('string')
        self.trakt = config.get('trakt', {'token': None,
                                          'token_date': None,
                                          'token_refresh': None})  # config.get('trakt', {}).get('token', None)
        self.provider = config.get('provider', 'thepiratebay')
        self.database = config.get('database', 'trakt')
        self.polishsource = config.get('polishsource', {'cookies': None})
        self.omdb_key = config.get('omdb_key', None)
        # self.save()  # save to add new values, correct structure etc.

    def save(self):
        # TODO: autosave on change any param
        config = {'destination': self.destination,
                  'quality': self.quality,
                  'min_size': self.min_size,
                  'score': self.score,
                  'trakt': self.trakt,
                  'provider': self.provider,
                  'database': self.database,
                  'polishsource': self.polishsource,
                  'omdb_key': self.omdb_key}
        yaml.safe_dump(config, open(self.config_file, 'w'), default_flow_style=False)
