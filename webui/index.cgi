#!/usr/bin/env python

# definitions
LIBRARY_URI = "/www/itunes.tommed.co.uk/Library.xml"
SONG_PREFIX_OLD = "file://localhost/Users/tom/Music/iTunes/"
SONG_PREFIX_NEW = "library/"

# error tracking through web interface
import cgitb, cgi
cgitb.enable()

# iTunes
from pyItunes import *
pl = XMLLibraryParser(LIBRARY_URI)
l = Library(pl.dictionary)

print "Content-Type: text/html\n\n"

print "<h1>iTunes Library</h1>"
print "<ul>"
for song in l.songs:
	location = song.location.replace(SONG_PREFIX_OLD,SONG_PREFIX_NEW)
	print "<li><a href=\"%s\">%s - %s</a></li>" % (location, song.artist, song.name)
print "</ul>"
