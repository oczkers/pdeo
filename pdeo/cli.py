# -*- coding: utf-8 -*-

"""
pdeo
====

Usage:
    pdeo [options]
    pdeo (mysql | sqlite) [options]

Options:
    -h, --help                          Show this screen.
    --version                           Show version.
    --debug                             Enable debug.
    -d DIR, --destination DIR           Destination dir for torrent files. [default: .]
    -q QUALITY, --quality QUALITY       Desired quality 720p/1080p/4k [default: 1080p]  # 4k might result in many fallpositives # TODO: resolution and bitrate instead? # TODO: codecs
    --min_size SIZE                     Mininmum size in GiB required. [default: 0]  # TODO: replace with bitrate, attach to quality.  # TODO?: max_size
    --strict                            Strict search, don't download if uncertain.  # TODO: implement this or somekind of score

Trakt options:

"""

# TODO: single movie search

import sys
from docopt import docopt

from . import __title__, __version__
from .core import Core


version_text = '%s v%s' % (__title__, __version__)


def run(database, destination, quality, min_size, debug):
    p = Core(database=database, debug=debug)
    p.get(destination=destination, quality=quality, min_size=min_size)


def __main__():
    args = docopt(__doc__, version=version_text)
    print(args)
    if args['mysql'] or args['sqlite']:
        # TODO: sql database
        # database = sql
        sys.exit('Mysql / Sqlite is not implementet yet.')
    else:
        database = 'trakt'
    run(database, destination=args['--destination'], quality=args['--quality'], min_size=int(args['--min_size']), debug=args['--debug'])


if __name__ == '__main__':
    __main__()
