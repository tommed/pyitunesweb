#!/usr/bin/env python

import cgi, cgitb
import sqlite3
import sys, os
cgitb.enable()

sys.path.append('../')
import settings

def install():
	"""install the sqlite3 database and install the schema"""
	print "<h2>Status</h2><pre>"
	print "- Deleting old database"
	os.system("rm "+settings.sqldb_file)
	print "- Creating new database file"
	conn = sqlite3.connect(settings.sqldb_file)
	print "- Creating database schema"
	conn.execute('''create table songs (hash text, artist text, track text, path text, album text)''')
	print "- Closing connection"
	conn.close()
	print "- Deleting old album art cache"
	os.system("rm %s/*.txt" % settings.artwork_path)
	print "Done"
	print '</pre><input type="button" value="add tracks..." onclick="document.location.href=\'scan.cgi\'"/>'

def main():
	form = cgi.FieldStorage()
	print "Content-Type: text/html\n"
	print "<!doctype html>"
	print "<html><body>"
	if form.getvalue('action') == "install":
		install()
	else:
		print "<h1>Installer</h1>"
		print "<p>Check the settings you have supplied are correct, then click the button below to create a database and start the import process of your data</p>"

		print "<h2>Settings</h2><ul>"
		print "<li>sqldbFile = %s</li>" % settings.sqldb_file
		print "</ul>"
		print '<input type="button" value="install..." onclick="document.location.href=\'index.cgi?action=install\'"/>'
	print "</body></html>"

if __name__ == "__main__":
	main()
