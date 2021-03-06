#!/usr/bin/env python
import sqlite3
import cgitb
import cgi
import md5, sys
cgitb.enable()

sys.path.append('../')
import settings
import albumart

# iTunes
from pyItunes import XMLLibraryParser, Library
pl = XMLLibraryParser(settings.itunes_library_file)
l = Library(pl)

# SQL db
sql=sqlite3.connect(settings.sqldb_file)

print "Content-Type: text/html\n\n"

print "<h1>iTunes Library</h1>"
print "<p>The following tracks have been added to your library:</p>"
print "<ul>"
song_count = 0
for song in l.songs:
	if not song.location.endswith(".mp3") and not song.location.endswith(".m4a"):
		continue
	# remove absolute file path from track path
	location = song.location.replace(l.options["Music Folder"], "")
	# see if track already exists
	md5hash=md5.new(song.artist+song.name).hexdigest()
	c=sql.cursor()
	count=c.execute("select count(hash) from songs where hash = ?", (md5hash,)).fetchone()[0]
	if count == 0:
		song_count += 1
		# track needs to be added
		sql.execute("insert into songs(hash,artist,track,path,album) values (?,?,?,?,?)",(md5hash,song.artist,song.name,location,song.album))
		print "<li><b>%s - %s</b> [%s]</li>" % (song.artist, song.name, song.album)
		albumart.getartwork(song.artist, song.album) # cache artwork
print "</ul>"
sql.commit()
sql.close()
print '<p>Added %d songs to your library. <a href="../">Proceed to your library</a></p>' % song_count

