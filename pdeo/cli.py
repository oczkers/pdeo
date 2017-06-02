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

Trakt options:
    -t TOKEN, --token TOKEN             OAuth token.

"""

from docopt import docopt

from . import __title__, __version__
from .database import database


version_text = '%s v%s' % (__title__, __version__)


def __main__():
    args = docopt(__doc__, version=version_text)
    print(args)
    if args['mysql'] or args['sqlite']:
        # TODO: sql database
        print('Mysql / Sqlite is not implementet yet.')
    else:
        print('trakt.')
        pass
    # if args['add']:
    #     db = database()
    #     if not db.add(tmdb_id=args['<tmdb_id>']):
    #         print('Movie already in database.')
    #     else:
    #         print('Movie added successfully.')


if __name__ == '__main__':
    __main__()
