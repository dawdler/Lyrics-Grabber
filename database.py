# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Lyrics Grabber - program to extract the lyrics of the song
# Copyright (c) 2014 - Atit Anand
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------


import sqlite3


class Database:
    def __init__(self):
        """Connect to lyrics database"""
        try:
            self.conn = sqlite3.connect('lyrics.db')
            # Artist/Song primary key because there is only one lyric song/artist
            self.conn.execute("""CREATE TABLE IF NOT EXISTS LyricsCache
            (artist TEXT NOT NULL,
            song TEXT NOT NULL,
            lyrics TEXT NOT NULL,
            PRIMARY KEY (artist, song));""")
            self.status = True  # Database ready to use, connection valid
        except sqlite3.DatabaseError:
            print "Something wrong with database"
            self.status = False

    def save(self, artist, song, lyrics):
        """Save the web-extracted lyrics"""
        self.conn.execute("INSERT INTO LyricsCache VALUES(?, ?, ?);", (artist, song, lyrics))
        self.conn.commit()

    def retrieve_lyrics(self, artist, song):
        """Returns lyrics or False if the lyrics are not in the database"""
        reply = self.conn.execute("SELECT lyrics FROM LyricsCache WHERE artist = ? AND song = ?;", (artist, song))
        rows = reply.fetchall()
        if len(rows) == 1:
            return rows[0][0]  # The artist/song lyrics - unpacking rows then row tuple
        else:
            return False  # No results found