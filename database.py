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


import psycopg2
import os

class Database:
    #TODO Implement the database stuffs using sqlite3. This would make the project more simpler.
    def __init__(self):
        '''connect to database holding the lyrics'''
        try:
            self.con = psycopg2.connect(database='lyrics', user='dawdler',port='5433')
            self.cur = self.con.cursor()
            #self.cur.execute("DROP TABLE IF EXISTS music")
            #check if the table is already created or not 
            self.cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('music',))
            if self.cur.fetchone()[0] is not True:
                self.cur.execute("CREATE TABLE music(artist VARCHAR(50) , song VARCHAR(50) PRIMARY KEY, contents BYTEA)")
                self.con.commit()
                #print "table created Successfully"
                self.status = True
        except psycopg2.DatabaseError, e:
            print 'Error %s' % e
            self.status = False

    def save_to_db(self, artist, song, data):
        '''save the extracted lyrics from web into database so that for the same request we don't have to search web. '''
        binary_data = psycopg2.Binary(data)
        self.cur.execute("INSERT INTO music(artist, song, contents) VALUES(%s,%s,%s)",(artist, song, binary_data))
        self.con.commit()

    def find_in_db(self, artist, song):
        '''Before searching web for lyrics, search into database. If found, return the lyrics'''
        self.cur.execute("SELECT * from music where artist=%s and song=%s",(artist,song))
        row = self.cur.fetchone()
        if row == None:
            #print "data not present"
            return -2
        else:
            return self.save_to_file(row[2])

    def save_to_file(self, lyrics):
        file = open("lyrics_temp.txt","wb")
        file.write(lyrics)
        file.close()
        file = open("lyrics_temp.txt","r")
        data = file.read()
        file.close()
        os.remove("lyrics_temp.txt")
        return data