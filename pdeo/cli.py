# -*- coding: utf-8 -*-

"""
pdeo.cli
~~~~~~~~~~~~~~~~

Usage:
    pdeo add <tmdb_id>

Options:
    -h --help   Show this screen.
    --version   Show version.

"""

from docopt import docopt

from .database import database


def __main__():
    args = docopt(__doc__)
    if args['add']:
        db = database()
        if not db.add(tmdb_id=args['<tmdb_id>']):
            print('Movie already in database.')
        else:
            print('Movie added successfully.')


if __name__ == '__main__':
    __main__()
