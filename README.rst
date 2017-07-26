====
pdeo
====

.. image:: https://img.shields.io/pypi/v/pdeo.svg
    :target: https://pypi.python.org/pypi/pdeo

.. image:: https://img.shields.io/pypi/l/pdeo.svg
    :target: https://pypi.python.org/pypi/pdeo

.. image:: https://img.shields.io/pypi/pyversions/pdeo.svg
    :target: https://pypi.python.org/pypi/pdeo

.. image:: https://travis-ci.org/oczkers/pdeo.png?branch=master
    :target: https://travis-ci.org/oczkers/pdeo

.. image:: https://codecov.io/github/oczkers/pdeo/coverage.svg?branch=master
    :target: https://codecov.io/github/oczkers/pdeo
    :alt: codecov.io

pdeo is a very simple alternative for radarr/couchpotato but using trakt as a watchlist database - automatically downloading movies from torrent.
It is written entirely in Python.



Documentation
=============

Documentation might be available someday at http://pdeo.readthedocs.org/.


Installation
============

(not working yet)

.. code-block:: bash

    computer ~ # pip install pdeo

OR download and invoke installation manually

.. code-block:: bash

    computer ~ # python setup.py install


Usage
=====

Look at pdeo/cli.py for more info.

.. code-block:: bash

    computer ~ # pdeo


Daemon
------

simple cronjob?

Drop show
---------

Simply hide show/season in trakt and we won't track it anymore.


List of providers
-----------------

- thepiratebay
- polishsource (private tracker)
- torrentday (private tracker) - not yet implemented


Development
===========


Provider
--------

Various bittorrent tracker websites.


License
-------

GNU GPLv3


.. image:: https://api.codacy.com/project/badge/Grade/042d79d8fb00475fa9903b24a1cce07c
   :alt: Codacy Badge
   :target: https://www.codacy.com/app/oczkers/pdeo?utm_source=github.com&utm_medium=referral&utm_content=oczkers/pdeo&utm_campaign=badger