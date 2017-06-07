# -*- coding: utf-8 -*-

"""
pdeo.config
~~~~~~~~~~~~~~~~~~~~~

This module implements the pdeo config methods.

"""

import yaml

from .exceptions import PdeoError


class Config(object):
    def __init__(self, config_file='pdeo.yml'):  # default filename
        self.config_file = config_file
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
        self.min_size = config.get('min_size', 0)
        self.trakt = config.get('trakt', {'token': None,
                                          'token_date': None,
                                          'token_refresh': None})  # config.get('trakt', {}).get('token', None)
        self.score = config.get('score', {'dead': -50,
                                          'trusted': 10,
                                          'vip': 20,
                                          'moderator': 50,
                                          'imdb': 50})  # TODO: custom score ('string')
        # self.save()  # save to add new values, correct structure etc.

    def save(self):
        config = {'destination': self.destination,
                  'quality': self.quality,
                  'min_size': self.min_size,
                  'trakt': self.trakt,
                  'score': self.score}
        yaml.safe_dump(config, open(self.config_file, 'w'), default_flow_style=False)
