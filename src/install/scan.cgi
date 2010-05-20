#!/usr/bin/env python
import sqlite3
import cgitb, cgi
import md5, sys
cgitb.enable()

sys.path.append('../')
import settings
# iTunes
from pyItunes import *
pl = XMLLibraryParser(settings.itunesLibraryFile)
l = Library(pl)

# SQL db
sql=sqlite3.connect(settings.sqldbFile)

print "Content-Type: text/html\n\n"

print "<h1>iTunes Library</h1>"
print "<p>The following tracks have been added to your library:</p>"
print "<ul>"
for song in l.songs:
	if not song.location.endswith(".mp3"):
		continue
	# remove absolute file path from track path
	location = song.location.replace(l.options["Music Folder"], "")
	# see if track already exists
	md5hash=md5.new(song.artist+song.name).hexdigest()
	c=sql.cursor()
	count=c.execute("select count(hash) from songs where hash = ?", (md5hash,)).fetchone()[0]
	if count == 0:
		# track needs to be added
		sql.execute("insert into songs(hash,artist,track,path) values (?,?,?,?)",(md5hash,song.artist,song.name,location))
		print "<li><a href=\"html5.cgi?s=%s\">%s - %s</a></li>" % (location, song.artist, song.name)
print "</ul>"
sql.commit()
sql.close()

