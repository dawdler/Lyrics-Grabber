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

import os
import sys
import requests
import subprocess

from gi.repository import Gtk
from database import Database
from gi.repository.Gdk import Color

class Lyrics:
	def gtk_main_quit(self, widget, data = None):
			self.remove_pidfile()
			Gtk.main_quit()

	def help_about(self, widget,data = None):
			result = self.about.run()
			self.about.hide()

	def link_click(self, widget,data = None):
			os.system("htmlview "+widget.get_uri())

	def new_search(self, widget, data = None):
		'''Users request for new search. Window should come back to initial state'''
		self.artist_name.set_text("")
		self.song_name.set_text("")
		self.status_bar.hide()
		self.lyrics_view.hide()
		self.scroll.hide()
		self.window.resize(self.width, self.height)
				
	def open_mp3(self, widget, data = None):
		'''Opens a mp3 file. Extracts artist name and song name and display the lyrics '''
		print "This feature will be implemented soon"


	def on_preference(self, widget, data = None):
		'''Dialog box will contains options likes settings for proxy server and all other settings '''
		print "This feature will be implemented soon"

	def is_running(self):
		pid = str(os.getpid())
		#dropping pid file to check already running instance
		pidfile = "/tmp/lyrics_grabber.pid"

		if os.path.isfile(pidfile):
		    print "Lyrics Grabber already running, exiting"
		    sys.exit(0)
		else:
		    file(pidfile, 'w').write(pid)
		    		
	def remove_pidfile(self):
		'''Remove the pid file'''
		pidfile = "/tmp/lyrics_grabber.pid"
		try:
			os.unlink(pidfile)
		except OSError:
			# Ignore the missing pid file
			pass

	def parse_input(self, artist, song):
	    valid = "0123456789abcdefghijklmnopqurstuvwxyz"
	    artist = ''.join([ch for ch in artist.lower() if ch in valid])
	    song = ''.join([ch for ch in song.lower() if ch in valid])
	    return artist, song

	def make_url(self, artist, song):
		'''Returns the url of the page from which lyrics will be extracted'''
		url = "http://www.azlyrics.com/lyrics/" + artist + "/" + song + ".html"
		return url

	def fetch_lyrics(self, url):
		'''Fetch the lyrics from azlyrics.com'''
		#data=requests.get(url,proxies=proxyDict) # will be used when internet is accessed via proxy server
		try:
			data = requests.get(url) #for accessing internet without proxy server
			data1 = data.content
			where_start = data1.find('<!-- start of lyrics -->')
			start = where_start + 26
			where_end = data1.find('<!-- end of lyrics -->')
			if where_start == -1 or  where_end == -1:
			    return -2
			end = where_end - 2
			lyrics = unicode(data1[start:end].replace('<br />', ''), "UTF8")
			lyrics = lyrics.replace('<i>','')
			lyrics = lyrics.replace('</i>','')
			return lyrics
	  	except:
	  		return -1
		

	def get_lyrics(self, widget, data = None):
		self.status_bar.hide()
		self.lyrics_view.hide()
		self.scroll.hide()
		self.artist, self.song = self.artist_name.get_text(), self.song_name.get_text()

		self.artist, self.song = self.parse_input(self.artist,
												  self.song)
		
		self.lyrics = -2
		found = False
		if self.database: #connected to database successfully
			self.lyrics = self.database.find_in_db(self.artist, self.song) # Search lyrics in database. If found, return lyrics
		if self.lyrics is -2:
			found = False
		else: 
			found = True
		
		if self.lyrics is -2:
			self.url = self.make_url(self.artist, self.song)
			self.lyrics = self.fetch_lyrics(self.url) # Not Found in database, fetch lyrics from web
			#print "Not found in database."
		context_id = self.status_bar.get_context_id("")
		self.status_bar.show()
		
		if self.lyrics == -2:			
			self.status_bar.push(context_id, "Lyrics Not Available")

		elif self.lyrics == -1:
			self.status_bar.push(context_id, "Network Connection Problem")

		else:
			self.scroll.show()
			self.lyrics_view.show()
			self.buffer = self.lyrics_view.get_buffer()
			#self.lyrics_view.set_text(self.lyrics)
			self.buffer.set_text(self.lyrics)
			if found is not True:
				#TODO directly convert UTF-8 to binary
				data = self.database.save_to_file(self.lyrics)
				self.database.save_to_db(self.artist, self.song, data) # save the extracted lyrics to database
			context_id = self.status_bar.get_context_id("")
			self.status_bar.push(context_id, "Lyrics Extracted Successfully")
		
	def __init__(self):
		self.is_running()
		self.database = Database()
		builder = Gtk.Builder()
		builder.add_from_file("lyrics_grabber.glade")
		self.window = builder.get_object("window1")
		self.window.set_resizable(False)
		self.window.set_title("Lyrics Grabber!")
		self.hbox1 = builder.get_object("box1")
		self.artist_name = builder.get_object("artist_name")
		self.song_name = builder.get_object("song_name")
		self.scroll = builder.get_object("scrolledwindow1")
		self.status_bar = builder.get_object("statusbar1")
		self.menubar = builder.get_object("menubar1")
		self.button = builder.get_object("get_lyrics")
		self.scroll.hide()

		self.lyrics_view = builder.get_object("textview1")
		self.lyrics_view.hide()
		self.width, self.height = self.window.get_size()
		self.about  = builder.get_object("aboutdialog1")
		builder.connect_signals(self)
		
		    
#=== EXECUTION ================================================================

if __name__ == "__main__":
	lyrics = Lyrics()
	lyrics.window.show()
	Gtk.main()