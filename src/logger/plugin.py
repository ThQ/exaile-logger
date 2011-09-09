# Copyright 2011 Thomas Quemard
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 3.0, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.


import logging
import os.path
import sqlite3
import time

VERSION = (0, 0, 1)
LOG = logging.getLogger(__name__)


class Store:
    def __init__ (self, store_path):
        LOG.debug("Opening SQLite database : %s", store_path)
        self.con = sqlite3.connect(store_path)
        self.cur = self.con.cursor()

    def check (self):
        in_shape = False
        for i in range(0, 2):
            if self.check_shape():
                in_shape = True

        if not in_shape:
            return False

        if self.check_version() == False:
            return False

        return True

    def check_shape (self):
        q = "SELECT COUNT(name) FROM sqlite_master"
        try:
            print self.cur.execute(q)
            res = self.cur.fetchone()
            if res[0] == 0:
                LOG.warning("DB does not contain any table.")
                self.setup()
                return False

        except sqlite3.OperationalError:
            LOG.warning("DB seems to be empty.")
            self.setup()

        return True

    def check_version (self):
        return self.get_info("version:major") != VERSION[0] and \
            self.get_info("version:minor") != VERSION[1]

    def get_info (self, name):
        self.cur.execute("SELECT value FROM _info WHERE name=\"version:major\"")
        return self.cur.fetchone()[0]

    def close (self):
        if self.con:
            self.con.close()

    def insert_log (self, file_url, song_artist, song_album, song_title, song_length, listened_for):
        LOG.debug("INSERT_LOG")
        listening_ratio = None
        if song_length and listened_for:
            listening_ratio = round(listened_for/song_length,2)

        q = """INSERT INTO history(date, file_url, song_artist, song_album,
        song_title, song_length, listened_for, listening_ratio)
        VALUES (strftime('%s','now'), ?, ?, ?, ?, ?, ?, ?)"""
        val = (file_url, song_artist, song_album, song_title, song_length, listened_for, listening_ratio)

        self.cur.execute(q, val)
        self.con.commit()

    def setup (self):
        LOG.debug("Setting up DB...")
        schema_file = open(os.path.join(os.path.dirname(__file__), "db_schema.sql"), "r")
        self.cur.executescript(schema_file.read())

        vals = []
        vals.append(("version:major", str(VERSION[0])))
        vals.append(("version:minor", str(VERSION[1])))
        for val in vals:
            self.cur.execute("INSERT INTO _info (name, value) VALUES (?, ?)", val)
        self.con.commit()

class Plugin:
    def __init__ (self, store_path):
        self.song = SongStatus()
        self.store = Store(store_path)
        self.panic = not self.store.check()

    def disable (self):
        if self.store:
            self.store.close()


class SongStatus:
    def __init__ (self):
        self.played_for = 0
        self.started_playing_at = None

