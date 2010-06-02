#!/usr/bin/env python
"""
=============================================
Ajax

This page provides an ajax end-point to this
application, so you can call methods from
javascript.
=============================================
"""
import json
import albumart
import cgi
import cgitb
import sqlite3
import settings
cgitb.enable()

print "Content-Type: application/javascript\n"

form = cgi.FieldStorage()

def ajax_get_artwork():
	"""returns the url for the artwork of the given album"""
	print "// "+form.getvalue('artist')
	print "// "+form.getvalue('album')
	print json.dumps({'src': albumart.get_artwork(form.getvalue('artist'), form.getvalue('album'))})

def ajax_list_artists():
	db=sqlite3.connect(settings.sqldb_file)
	result = [row[0] for row in db.execute('select distinct artist from songs order by artist')]
	print json.dumps(result)

def main():
	"""main entry point for this page"""
	method = form.getvalue('method').lower()
	if method == 'artwork.get':
		ajax_get_artwork()
	elif method == 'artist.list':
		ajax_list_artists()
	else:
		 print json.dumps({ 'error': "Method %s not recognised" % method })

if __name__ == "__main__":
	main()

# vim: cin ai sw=2 ts=2
