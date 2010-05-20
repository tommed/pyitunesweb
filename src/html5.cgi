#!/usr/bin/env python

import cgi
form = cgi.FieldStorage()

print "Content-Type: text/html\n\n"
print "<!doctype html>\n"
print "<html><body>"
print "<audio src=\"serve.cgi?s=%s\" controls autobuffer autoplay/>" % form['s'].value
print "</body></html>"
