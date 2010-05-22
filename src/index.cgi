#!/usr/bin/env python
import sqlite3
import settings
import cgi, cgitb
cgitb.enable()

form = cgi.FieldStorage()


sql=sqlite3.connect(settings.sqldbFile)


def calculatePaging():
	"""determine the number of pages, and other values which are required
	to get paging to work"""
	trackCount = sql.execute("select count(*) from songs").fetchone()[0]
	if "search" in form and (form.getvalue('search')) > 0:
		trackCount = sql.execute("select count(*) from songs where artist like '%{0}%' or track like '%{0}%'".format(form.getvalue('search'))).fetchone()[0]
	pageNumber = 1
	if "page" in form:
		pageNumber = int(form.getvalue('page'))
	pageCount = int(trackCount / settings.pageLimit)
	if trackCount % settings.pageLimit != 0:
		pageCount += 1
	offset = int((pageNumber-1) * settings.pageLimit)
	return (trackCount,pageCount,offset,pageNumber)


trackCount,pageCount,offset,pageNumber = calculatePaging()
searchDefault = ""
sqlcmd = "select * from songs order by artist,track limit %d offset %d" % (settings.pageLimit, offset)
if "search" in form and len(form.getvalue('search')) > 0:
	query = form.getvalue('search')
	searchDefault = query
	sqlcmd = "select * from songs where artist like '%{0}%' or track like '%{0}%' order by artist,track limit {1} offset {2}".format(query, settings.pageLimit, offset)

tcursor = sql.execute(sqlcmd)

print "Content-Type: text/html\n"
print '''<!doctype html>
 <html lang="en">
 <head>
   <title>pyitunesweb | github.com/tommed/pyitunesweb</title>
   <style type="text/css">
    .player { position: absolute; top: 10px; right: 10px; }
   </style>
  <script>
	icon = 'images/track.png'
	function $(elem) { return document.getElementById(elem); }
	function play(src, artist, track) { 
	  $('player').src = "%siTunes Music/"+src
	  $('player').load()
	  $('player').play() 
	  show_notification(artist, track)
	}
	function show_notification(artist, track) {
	  if (window.webkitNotifications.checkPermission() == 0) {
		window.webkitNotifications.createNotification(icon, artist, track).show()
	  } else {
		window.webkitNotifications.requestPermission();
	  }
	}
  </script>
 </head>
 <body>
 <div class="player"><audio id="player" controls autobuffer autoplay/></div>''' % settings.publicItunesPath
#print "<pre>%s</pre>" % sqlcmd
print "Track Count: %d" % trackCount
print '<a href="install/scan.cgi">Scan</a>'
print '<h2>Search</h2>'
print '<form method="get" action="index.cgi"><input type="search" name="search" value="%s" results="5"/>' % searchDefault
print '</form>'
print '<h2>Songs</h2>'
print "<ul>"
for song in tcursor:
	print '<li><a href="javascript:play(\'{0}\', \'{1}\', \'{2}\');">{1} - {2}</a></li>'.format(song[3].replace("'","\\'"),song[1].replace("'","\\'"),song[2].replace("'","\\'"))
print "</ul>"
if pageCount > 0:
	print "<p>Page %d of %d</p>" % (pageNumber, pageCount)
	if pageNumber > 1:
		print '<a href="index.cgi?page=%d&search=%s">&lt; Previous</a>' % (pageNumber-1, searchDefault)
	if pageNumber != pageCount:
		print '<a href="index.cgi?page=%d&search=%s">Next &gt;</a>' % (pageNumber+1, searchDefault)
print "</body></html>"
