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
    --strict                            Strict search, don't download if uncertain.  # TODO: implement

Trakt options:
    -t TOKEN, --token TOKEN             OAuth token.

"""

# TODO: single movie search

from docopt import docopt

from . import __title__, __version__
from .core import Core


version_text = '%s v%s' % (__title__, __version__)


def __main__():
    args = docopt(__doc__, version=version_text)
    print(args)
    if args['mysql'] or args['sqlite']:
        # TODO: sql database
        print('Mysql / Sqlite is not implementet yet.')
    else:
        print('trakt.')
        p = Core()
        print(p.check('logan', 2017))
    # if args['add']:
    #     db = database()
    #     if not db.add(tmdb_id=args['<tmdb_id>']):
    #         print('Movie already in database.')
    #     else:
    #         print('Movie added successfully.')


if __name__ == '__main__':
    __main__()
