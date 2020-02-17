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
    --debug                             Enable debug.  # TODO: enable debug automatically if not daemon
    --daemon                            Daemon mode - runs every 24hours and not printing anything.
    -c FILE, --config FILE              Config file. [default: ~/.config/pdeo.yml]  # TODO: implement
    -d DIR, --destination DIR           Destination dir for torrent files. [default: .]
    -q QUALITY, --quality QUALITY       Desired quality 720p/1080p/2160p  # TODO: resolution and bitrate instead? # TODO: codecs
    --min_size SIZE                     Mininmum size in GiB required. [default: 6]  # TODO: separate min_size for shows # TODO: replace with bitrate, attach to quality.  # TODO?: max_size
    --strict                            Strict search, don't download if uncertain.  # TODO: implement this or somekind of score
    -p PROVIDER, --provider PROVIDER    Choose provider.
    -U USERNAME, --user USERNAME        Provider username (needed only once).
    -P PASSWORD, --password PASSWORD    Provider password (needed only once).

Trakt options:

"""

# TODO: single movie search

# import sys
import argparse

from . import __title__, __version__
from .core import Core


version_text = '%s v%s' % (__title__, __version__)


def run(provider, database, destination, quality, min_size, debug, username, passwd):
    p = Core(database=database, provider=provider, debug=debug, username=username, passwd=passwd)
    p.get(destination=destination, quality=quality, min_size=min_size)
    p.getShows(destination=destination, quality=quality, min_size=min_size / 2)


def __main__():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--debug', action="store_true", default=False)
    parser.add_argument('--daemon', action="store_true", default=False)
    parser.add_argument('-c', '--config', default='~/.config/pdeo.yml')
    parser.add_argument('-d', '--destination', default='.')
    parser.add_argument('-q', '--quality')
    parser.add_argument('--min_size', type=int, default=6)
    parser.add_argument('--strict', action="store_true", default=False)
    parser.add_argument('-p', '--provider')
    parser.add_argument('-U', '--user')
    parser.add_argument('-P', '--password')
    args = parser.parse_args()
    print(args)
    # if args['mysql'] or args['sqlite']:
    #     # TODO: sql database
    #     # database = sql
    #     sys.exit('Mysql / Sqlite is not implementet yet.')
    # else:
    #     database = 'trakt'
    database = 'trakt'
    run(provider=args.provider,
        database=database,
        destination=args.destination,
        quality=args.quality,
        min_size=args.min_size,
        debug=args.debug,
        username=args.user,
        passwd=args.password)


if __name__ == '__main__':
    __main__()
