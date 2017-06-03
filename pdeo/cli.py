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
from docopt import docopt

from . import __title__, __version__
from .core import Core
from .databases import trakt


version_text = '%s v%s' % (__title__, __version__)


def run(database):
    p = Core(database=database)
    print(p.get('logan', 2017, 'tt3315342'))


def __main__():
    args = docopt(__doc__, version=version_text)
    print(args)
    if args['mysql'] or args['sqlite']:
        # TODO: sql database
        # database = sql
        sys.exit('Mysql / Sqlite is not implementet yet.')
    else:
        database = trakt
    run(database)


if __name__ == '__main__':
    __main__()
