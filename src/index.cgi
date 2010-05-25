#!/usr/bin/env python
# vim: cin ai sw=2 ts=2
import sqlite3
import settings
import cgi
import cgitb
import albumart

# handle exceptions over the web
cgitb.enable()

# templating engine
import tenjin 
from tenjin.helpers import to_str, escape
engine = tenjin.Engine()

# querystring and post fields
form = cgi.FieldStorage()

# sql data for tracks
sql=sqlite3.connect(settings.sqldb_file)

def calculatePaging():
	"""determine the number of pages, and other values which are required
		 to get paging to work.
		 """
	track_count = sql.execute("select count(*) from songs").fetchone()[0]
	if "search" in form and form.getvalue('search'):
		track_count = sql.execute("select count(*) from songs where artist like '%{0}%' or track like '%{0}%' or album like '%{0}%'".format(form.getvalue('search'))).fetchone()[0]
	page_number = 1
	if "page" in form:
		page_number = int(form.getvalue('page'))
	page_count = int(track_count / settings.page_limit)
	if track_count % settings.page_limit != 0:
		page_count += 1
	offset = int((page_number-1) * settings.page_limit)
	return (track_count,page_count,offset,page_number)

def get_album_artwork(song, lastalbum):
	result = ''
	if song[4] != lastalbum:
		result = '<h3><img src="{0}" alt="{1} {2}"/>{1} - {2}</h3></li><li>'\
						.format(albumart.get_artwork(song[1],song[4]), song[1], song[4])
	lastalbum = song[4]
	return result

def main():
	"""main entry point for this page"""
	track_count,page_count,offset,page_number = calculatePaging()
	search_default = ""
	sqlcmd = "select * from songs order by album,artist limit %d offset %d" % (settings.page_limit, offset)
	if "search" in form and len(form.getvalue('search')) > 0:
		query = form.getvalue('search')
		search_default = query
		sqlcmd = "select * from songs where artist like '%{0}%' or track like '%{0}%' or album like '%{0}%' order by album,artist limit {1} offset {2}".format(query, settings.page_limit, offset)
	tcursor = sql.execute(sqlcmd)
	context={
		"pitpath":settings.public_itunes_path, 
		"songs":tcursor, 
		"search_default":search_default, 
		"track_count":track_count,
		"page_number":page_number,
		"page_count":page_count,
	}
	print "Content-Type: text/html\n"
	print engine.render("index.cgi.pyhtml", context)

if __name__ == "__main__":
	main()
