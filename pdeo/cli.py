# -*- coding: utf-8 -*-

"""
pdeo
====

Usage:
    pdeo [-t TOKEN] [options]
    pdeo (mysql | sqlite) [options]

Options:
    -h, --help                          Show this screen.
    --version                           Show version.
    -d DIR, --destination DIR           Destination dir for torrent files [default: .]
    -q QUALITY, --quality QUALITY       Desired quality rhd/hd/uhd [default: hd] - doesn't work yet  # TODO: resolution and bitrate instead?
    --strict                            Strict search, don't download if uncertain.  # TODO: implement this or somekind of score

Trakt options:
    -t TOKEN, --token TOKEN             OAuth token.

"""

# TODO: single movie search

import sys
import yaml
from docopt import docopt

from . import __title__, __version__
from .core import Core

if sys.version_info[0] == 2:
    FileNotFoundError = IOError


version_text = '%s v%s' % (__title__, __version__)

config_file = 'pdeo.yml'


# pathlib?
try:
    config = yaml.safe_load(open(config_file, 'r'))
except FileNotFoundError as e:
    print(e)  # config does not exists, load default
    config = {
        'trakt': {'token': None,
                  'token_date': None,
                  'token_refresh': None}
    }
except yaml.YAMLError as e:
    print(e)  # config cannot be loaded


print(config)
yaml.safe_dump(config, open(config_file, 'w'), default_flow_style=False)


def run(database):
    p = Core(database=database)
    p.get()


def __main__():
    args = docopt(__doc__, version=version_text)
    print(args)
    if args['mysql'] or args['sqlite']:
        # TODO: sql database
        # database = sql
        sys.exit('Mysql / Sqlite is not implementet yet.')
    else:
        database = 'trakt'
    run(database)


if __name__ == '__main__':
    __main__()
