#!/usr/bin/env python
import settings

# definitions
SONG_PREFIX_NEW = "library/"

# error tracking through web interface
import cgitb, cgi
cgitb.enable()

# iTunes
from pyItunes import *
pl = XMLLibraryParser(settings.itunesLibraryFile)
l = Library(pl)

print "Content-Type: text/html\n\n"

print "<h1>iTunes Library</h1>"
print "<ul>"
for song in l.songs:
	if not song.location.endswith(".mp3"):
		continue
	location = song.location.replace(l.options["Music Folder"], "")
	print "<li><a href=\"serve.cgi?s=%s\">%s - %s</a></li>" % (location, song.artist, song.name)
print "</ul>"
