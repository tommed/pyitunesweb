#!/usr/bin/env python

import settings
import cgi
form = cgi.FieldStorage()

print "Content-Type: text/html\n\n"
print "<!doctype html>\n"
print "<html><body>"
print "<audio src=\"%siTunes Music/%s\" controls autobuffer autoplay/>" % (settings.publicItunesPath, form['s'].value)
print "</body></html>"
