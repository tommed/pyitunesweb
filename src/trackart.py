import settings
import urllib2, urllib
import re
from cgi import escape
import md5
import os

def getartwork(artist, track, size="small"):
	hash = md5.new(str(artist)+str(track)).hexdigest()
	path = settings.artworkpath+"/"+hash+".txt"
	if os.path.exists(path):
		return open(path, 'r').read()
	else:
	 url = getartworkurl(artist, track, size)
	 io=open(path, 'w')
	 io.write(url)
	 io.close()
	 return url
	

def getartworkurl(artist, track, size="small"):
	url = "http://ws.audioscrobbler.com/2.0/?method=track.getinfo&api_key=%s&artist=%s&track=%s" % (settings.lastfmApiKey, urllib.quote(artist), urllib.quote(track))
	#print url
	req=urllib2.Request(url)
	req.add_header("User-Agent", "Mozilla/5.0")
	try:
		io=urllib2.urlopen(req)
		resultxml=io.read(300)
	except:
		resultxml = ""
	resultre=re.search("<image size=\"%s\">(.*)</image>" % size,resultxml)
	if resultre == None:
		return "images/track.png"
	else:
		return resultre.group(1)


#print getartworkurl("Bessie Smith", "Careless Love")

# vim: cin ai sw=2 ts=2
