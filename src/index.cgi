#!/usr/bin/env python
# vim: cin ai sw=2 ts=2
import sqlite3
import settings
import cgi, cgitb
import albumart
cgitb.enable()

# templating engine
import tenjin 
from tenjin.helpers import *
engine = tenjin.Engine()

# querystring and post fields
form = cgi.FieldStorage()

# sql data for tracks
sql=sqlite3.connect(settings.sqldbFile)

def calculatePaging():
	"""determine the number of pages, and other values which are required
	to get paging to work"""
	trackCount = sql.execute("select count(*) from songs").fetchone()[0]
	if "search" in form and (form.getvalue('search')) > 0:
		trackCount = sql.execute("select count(*) from songs where artist like '%{0}%' or track like '%{0}%' or album like '%{0}%'".format(form.getvalue('search'))).fetchone()[0]
	pageNumber = 1
	if "page" in form:
		pageNumber = int(form.getvalue('page'))
	pageCount = int(trackCount / settings.pageLimit)
	if trackCount % settings.pageLimit != 0:
		pageCount += 1
	offset = int((pageNumber-1) * settings.pageLimit)
	return (trackCount,pageCount,offset,pageNumber)

def artwork(artist, album):
	return albumart.getartwork(artist, album)

def albumartwork(song, lastalbum):
	start = ''
	end = ''
	if song[4] != lastalbum:
		start = '<h3><img src="{0}" alt="{1} {2}"/>{1} - {2}</h3></li><li>'.format(artwork(song[1],song[4]), song[1], song[4])
	lastalbum = song[4]
	return start,end

# main
trackCount,pageCount,offset,pageNumber = calculatePaging()
searchDefault = ""
sqlcmd = "select * from songs order by album,artist limit %d offset %d" % (settings.pageLimit, offset)
if "search" in form and len(form.getvalue('search')) > 0:
	query = form.getvalue('search')
	searchDefault = query
	sqlcmd = "select * from songs where artist like '%{0}%' or track like '%{0}%' or album like '%{0}%' order by album,artist limit {1} offset {2}".format(query, settings.pageLimit, offset)
tcursor = sql.execute(sqlcmd)

context={
	"pitpath":settings.publicItunesPath, 
	"songs":tcursor, 
	"searchDefault":searchDefault, 
	"trackCount":trackCount,
	"pageNumber":pageNumber,
	"pageCount":pageCount,
	"artwork":artwork,
}

print "Content-Type: text/html\n"
print engine.render("index.cgi.pyhtml", context)
