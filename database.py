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
import os

class Database:
    def __init__(self):
        '''connect to database holding the lyrics'''
        try:
            self.conn = sqlite3.connect('music.db')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS Lyrics
            (artist           TEXT    NOT NULL,
            song          TEXT    NOT NULL,
            contents       BYTEA);''')
            self.status = True #table created successfully
        except:
            print "Something wrong with database"
            self.status = False

    def save_to_db(self, artist, song, data):
        '''save the extracted lyrics from web into database so that for the same request we don't have to search web. '''
        binary_data = sqlite3.Binary(data)
        self.conn.execute("INSERT INTO Lyrics VALUES(?, ?, ?);",(artist, song, binary_data))
        self.conn.commit()

    def find_in_db(self, artist, song):
        '''Before searching web for lyrics, search into database. If found, return the lyrics'''
        rows = self.conn.execute("SELECT * from Lyrics where artist = ? and song = ?",(artist, song))
        for row in rows:
            return self.save_to_file(row[2])        
        return -2
        
    def save_to_file(self, lyrics):
        file = open("lyrics_temp.txt","wb")
        file.write(lyrics)
        file.close()
        file = open("lyrics_temp.txt","r")
        data = file.read()
        file.close()
        os.remove("lyrics_temp.txt")
        return data