import settings
import urllib2
from urllib import quote
import re
from cgi import escape
import md5
import os

DEFAULT_ARTWORK = "images/track.png"

def get_artwork(artist, album, size="medium"):
	"""looks in the cache directory for the url for the album art, if it
		 isn't present; then last.fm is called and the artwork is requested
		 then cached.
		 If the album isn't set, then the default artwork is returned.
		 """
	if album == None:
		return DEFAULT_ARTWORK
	hash = md5.new(str(artist)+str(album)).hexdigest()
	path = settings.artwork_path+"/"+hash+".txt"
	if os.path.exists(path):
		return open(path, 'r').read()
	else:
	 url = get_artwork_from_lastfm(artist, album, size)
	 io=open(path, 'w')
	 io.write(url)
	 io.close()
	 return url
	

def get_artwork_from_lastfm(artist, album, size):
	"""uses the last.fm album.getinfo api to retrieve the url for the album art
		 if this can't be found, then it will return some default artwork.
		 """
	if album == None:
		return DEFAULT_ARTWORK
	url = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=%s&artist=%s&album=%s"\
				 % (settings.lastfm_apikey, quote(artist), quote(album))
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


#print get_artwork_from_lastfm("Adele", "19", "large")
# vim: cin ai sw=2 ts=2
