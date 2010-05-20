#!/usr/bin/env python
import sqlite3
import settings
import cgi, cgitb
cgitb.enable()

form = cgi.FieldStorage()


sql=sqlite3.connect(settings.sqldbFile)
trackCount = sql.execute("select count(*) from songs").fetchone()[0]
pageNumber = 1
if "page" in form:
	pageNumber = int(form.getvalue('page'))
pageCount = int(trackCount / settings.pageLimit)
if trackCount % settings.pageLimit != 0:
	pageCount += 1
offset = int((pageNumber-1) * pageCount)

tcursor = sql.execute("select * from songs order by artist,track limit %d offset %d" % (settings.pageLimit, offset))

print "Content-Type: text/html\n"
print "<!doctype html>"
print "<body>"
print "Track Count: %d" % trackCount
print "<ul>"
for song in tcursor:
	print '<li><a href="html5.cgi?s=%s">%s - %s</a></li>' % (song[3],song[1],song[2])
print "</ul>"
if pageNumber > 1:
	print '<a href="index.cgi?page=%d">&lt; Previous</a>' % (pageNumber-1)
print '<a href="index.cgi?page=%d">Next &gt;</a>' % (pageNumber+1)
print "</body>"
