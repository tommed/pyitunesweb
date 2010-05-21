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
print "<!doctype html>"
print "<body>"
#print "<pre>%s</pre>" % sqlcmd
print "<p>Track Count: %d</p>" % trackCount
print '<form method="get" action="index.cgi"><input type="search" name="search" value="%s" results="5"/>' % searchDefault
print '</form>'
print "<ul>"
for song in tcursor:
	print '<li><a href="html5.cgi?s=%s">%s - %s</a></li>' % (song[3],song[1],song[2])
print "</ul>"
if pageCount > 0:
	print "<p>Page %d of %d</p>" % (pageNumber, pageCount)
	if pageNumber > 1:
		print '<a href="index.cgi?page=%d&search=%s">&lt; Previous</a>' % (pageNumber-1, searchDefault)
	if pageNumber != pageCount:
		print '<a href="index.cgi?page=%d&search=%s">Next &gt;</a>' % (pageNumber+1, searchDefault)
print "</body>"
