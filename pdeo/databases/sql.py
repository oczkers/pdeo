# -*- coding: utf-8 -*-

"""
pdeo.database.sql
~~~~~~~~~~~~~~~~~~~~~

This module implements the pdeo sql backend for database methods.

"""

# TODO: mysql

import sqlite3


class Database(object):
    def __init__(self):
        self.db = self.load()
        self.create()  # TODO: create only if not existing DEBUG

    def load(self):
        """Loads database."""
        # TODO: catch exceptions
        con = sqlite3.connect('pdeo.db')
        con.isolation_level = None  # autocommit
        return con.cursor()

    def create(self):  # private?
        """Creates database structure."""
        self.db.execute('''CREATE TABLE IF NOT EXISTS pdeo (
            id INTEGER PRIMARY KEY,
            title,
            tmdb_id UNIQUE
        )''')

    def add(self, tmdb_id):
        """Add movie to database."""
        # TODO: check if not a duplicate
        try:
            self.db.execute(f'INSERT INTO pdeo (tmdb_id) VALUES ({tmdb_id})')
        except sqlite3.IntegrityError:  # duplicate
            return False
        return True
