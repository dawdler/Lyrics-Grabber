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
import re

import requests
from gi.repository import Gtk

from database import Database


class LyricsApplication():
    def __init__(self):
        self.is_running()
        self.database = Database()
        self.builder = Gtk.Builder()
        self.builder.add_from_file("app.glade")

        self.window = self.builder.get_object("MainWindow")
        self.hbox1 = self.builder.get_object("menu_box")
        self.artist_name = self.builder.get_object("artist_entry")
        self.song_name = self.builder.get_object("song_entry")
        self.scroll = self.builder.get_object("lyrics_scroll_container")
        self.status_bar = self.builder.get_object("statusbar")
        self.menubar = self.builder.get_object("menu")
        self.button = self.builder.get_object("get_lyrics_button")
        self.lyrics_view = self.builder.get_object("lyrics_display")
        self.about = self.builder.get_object("about")

        self.window.set_resizable(False)
        self.scroll.hide()
        self.lyrics_view.hide()
        self.width, self.height = self.window.get_size()

        # Connect to signals
        self.builder.connect_signals(self)

        # Define accelerator keys
        self._init_accelerators()


    def _init_accelerators(self):
        """Initialize gtk accelerators for different interface elements"""
        accel_group = Gtk.AccelGroup()
        self.builder.get_object("MainWindow").add_accel_group(accel_group)
        self._add_accelerator_for_widget(accel_group, "new_s", "<Control>n")
        self._add_accelerator_for_widget(accel_group, "open_s", "<Control>o")
        self._add_accelerator_for_widget(accel_group, "quit_s", "<Control>q")
        self._add_accelerator_for_widget(accel_group, "pref_s", "<Control>p")
        self._add_accelerator_for_widget(accel_group, "about_s", "F1")

    def _add_accelerator_for_widget(self, accel_group, name, accel):
        widget = self.builder.get_object(name)
        key, mod = Gtk.accelerator_parse(accel)
        widget.add_accelerator("activate", accel_group, key, mod, Gtk.AccelFlags.VISIBLE)

    def gtk_main_quit(self, widget, data=None):
        self.remove_pidfile()
        Gtk.main_quit()

    def help_about(self, widget, data=None):
        result = self.about.run()
        self.about.hide()

    def link_click(self, widget, data=None):
        os.system("htmlview " + widget.get_uri())

    def new_search(self, widget, data=None):
        """Users request for new search. Window should come back to initial state"""
        self.artist_name.set_text("")
        self.song_name.set_text("")
        self.status_bar.hide()
        self.lyrics_view.hide()
        self.scroll.hide()
        self.window.resize(self.width, self.height)

    def open_mp3(self, widget, data=None):
        """Opens a mp3 file. Extracts artist name and song name and display the lyrics """
        print "This feature will be implemented soon"


    def on_preference(self, widget, data=None):
        """Dialog box will contains options likes settings for proxy server and all other settings """
        print "This feature will be implemented soon"

    def is_running(self):
        pid = str(os.getpid())
        # dropping pid file to check already running instance
        pidfile = "/tmp/lyrics_grabber.pid"

        if os.path.isfile(pidfile):
            print "Lyrics Grabber already running, exiting"
            sys.exit(0)
        else:
            file(pidfile, 'w').write(pid)

    def remove_pidfile(self):
        """Remove the pid file"""
        pidfile = "/tmp/lyrics_grabber.pid"
        try:
            os.unlink(pidfile)
        except OSError:
            # Ignore the missing pid file
            pass

    def clean_user_input(self, user_input):
        """Deletes any illegal characters for urls"""
        legal_chars = re.compile(r'^[a-z0-9]$')
        return filter(lambda c: re.match(legal_chars, c), user_input.lower())

    def make_url(self, artist, song):
        """Returns the url of the page from which lyrics will be extracted"""
        url = "http://www.azlyrics.com/lyrics/{}/{}.html".format(artist, song)
        return url

    # This code is pretty hacky, we should try to clean it up. It works though.
    def fetch_lyrics(self, url):
        """Fetch the lyrics from azlyrics.com"""
        # data=requests.get(url,proxies=proxyDict) # will be used when internet is accessed via proxy server
        data = requests.get(url)  # for accessing internet without proxy server
        data1 = data.content
        where_start = data1.find('<!-- start of lyrics -->')
        start = where_start + 26
        where_end = data1.find('<!-- end of lyrics -->')
        if where_start == -1 or where_end == -1:
            return False
        end = where_end - 2
        lyrics = unicode(data1[start:end].replace('<br />', ''), "UTF8")
        lyrics = lyrics.replace('<i>', '')
        lyrics = lyrics.replace('</i>', '')
        return lyrics

    def display_message(self, message):
        """Displays the message in a pop up status bar"""
        context_id = self.status_bar.get_context_id("")
        self.status_bar.show()
        self.status_bar.push(context_id, message)


    def get_lyrics(self, widget, data=None):
        """Retrieves the lyrics for a given artist and song. First checks for lyrics in database,
        and if not found grabs the lyrics from the web."""

        # Disable lyrics display
        self.status_bar.hide()
        self.lyrics_view.hide()
        self.scroll.hide()

        # Parse user input
        artist = self.clean_user_input(self.artist_name.get_text())
        song = self.clean_user_input(self.song_name.get_text())

        lyrics = None
        in_database = False

        if self.database.status:  # Testing connection to database
            lyrics = self.database.retrieve_lyrics(artist, song)
            if lyrics:  # False if not found in database
                in_database = True

        if not lyrics:  # Try next to retrieve from web
            url = self.make_url(artist, song)
            try:
                lyrics = self.fetch_lyrics(url)
            except:
                self.display_message('Internet Connection Problem') # Could not connect to internet
                return

        if not lyrics:  # Not available in database or on web
            self.display_message('Lyrics Not Available')
        else:
            # Set the display
            lyrics_buffer = self.lyrics_view.get_buffer()
            lyrics_buffer.set_text(lyrics)

            if not in_database: # Save if not in database
                self.database.save(artist, song, lyrics)

            # Re-enable lyrics display
            self.scroll.show()
            self.lyrics_view.show()
            self.display_message('Lyrics Extracted Successfully')

# === EXECUTION ================================================================
if __name__ == "__main__":
    app = LyricsApplication()
    app.window.show()
    Gtk.main()
