import settings
import urllib2, urllib
import re
from cgi import escape
import md5
import os

def getartwork(artist, album, size="medium"):
	if album == None:
		return "images/track.png"
	hash = md5.new(str(artist)+str(album)).hexdigest()
	path = settings.artworkpath+"/"+hash+".txt"
	if os.path.exists(path):
		return open(path, 'r').read()
	else:
	 url = getartworkurl(artist, album, size)
	 io=open(path, 'w')
	 io.write(url)
	 io.close()
	 return url
	

def getartworkurl(artist, album, size):
	if album == None:
		return "images/track.png"
	url = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=%s&artist=%s&album=%s" % (settings.lastfmApiKey, urllib.quote(artist), urllib.quote(album))
	#print url
	req=urllib2.Request(url)
	req.add_header("User-Agent", "Mozilla/5.0")
	try:
		io=urllib2.urlopen(req)
		resultxml=io.read(600)
	except:
		#print "except!"
		resultxml = ""
	#print resultxml
	resultre=re.search("image size=\"%s\".(.*)</image" % size,resultxml)
	if resultre == None or len(resultre.group(1)) == 0:
		return "images/track.png"
	else:
		return resultre.group(1)


#print getartworkurl("Adele", "19", "large")
# vim: cin ai sw=2 ts=2
