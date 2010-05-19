#!/usr/bin/env python

import settings
import cgitb, cgi
cgitb.enable()

mime = {
	".mp4":"audio/mp4",
	".m4a":"application/octet-stream",
	".mp3":"audio/mpeg3"
}

form = cgi.FieldStorage()
location = settings.itunesPath+"/iTunes Music/"+str(form['s'].value)

#print "Content-Type: text/plain\n\n"
#print mime[location[-4:]]

#"""
buffer = file(location, 'r').read()
content_type = mime[location[-4:]]
print "Content-Type: %s\nContent-Length:%s\n\n" % (content_type, len(buffer))
print buffer
#"""
