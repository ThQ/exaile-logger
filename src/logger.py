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


LOG = logging.getLogger(__name__)


class Store:
    def __init__ (self, store_path):
        LOG.debug("Opening SQLite database : %s", store_path)
        self.con = sqlite3.connect(store_path)
        self.cur = self.con.cursor()

    def close (self):
        if self.con:
            self.con.close()

    def insert_log (self, file_url, song_artist, song_album, song_title, song_length, listened_for):
        q = """INSERT INTO history(date, file_url, song_artist, song_album,
        song_title, song_length, listened_for)
        VALUES (strftime('%s','now'), ?, ?, ?, ?, ?, ?)"""
        val = (file_url, song_artist, song_album, song_title, song_length, listened_for)

        self.cur.execute(q, val)
        self.con.commit()


class Plugin:
    def __init__ (self, store_path):
        self.song = SongStatus()
        self.logger = Logger()
        self.store = Store(store_path)

    def disable (self):
        self.logger.disable()
        self.store.close()


class SongStatus:
    def __init__ (self):
        self.played_for = 0
        self.started_playing_at = None


class Logger:
    def __init__ (self):
        pass

    def disable (self):
        if self.file:
            self.file.close()
