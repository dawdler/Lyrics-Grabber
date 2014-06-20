# Lyrics Grabber

Lyrics Grabber! A simple lyrics grabber application for Linux. Successfully grabs lyrics from web and stores it in database.

## Dependencies

	* python 2.7 or above
	* python-psycopg2
	* pyGTK
	* python-requests

## Setup

First, Install the above dependencies.

Second, you'll need to create a postgresql database where Lyrics Grabber can store the lyrics. For example, on your local setup:

	$ sudo -u postgres createuser dawdler(ownner of the database)

	$ sudo -u postgres createdb lyrics -O dawdler

Replace owner of the database `dawdler` with yours in the source code.

## Running

To run Lyrics Grabber, execute it directly from the source folder:
	
	$ cd Lyrics-Grabber/
	$ python lyrics_grabber.py

## Future

Well, this is simple summer project started  so that I could get better with python, gtk, dbus, databases and all other stuffs. This project is in very initial stage right now. Lots of many features can be added to the application like:

	* Applications grabs lyrics from only one website as of now i.e `www.azlyrics.com`. Other sources can be added as well.
	* Preference class that will hold the necessary settings needed to run the application.
	* Improve the look and feel of the UI.
	* Extracting artist/song name by opening a music file.
	* Display the lyrics of the currently running song in banshee, rhythmbox, etc.
	* Remove the existing bugs from the application.
	* Tagging lyrics in the music file itself.

Lots of more features can be thought and added. Hopefully will be adding few of them whenever I get time.

## Contributions

Interested people are always free to contribute. Think of new features or something, feel free to code it up. Send merge requests, make sure you update AUTHORS and CHANGELOG. Beginners can easily understand this open source project. Anyone willing to improve their skills, can contribute to the project. Well, I am also a beginner. 

Thanks for using Lyrics Grabber! Cheers!
