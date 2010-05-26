
// !!! Todo: change this to the album's artwork
var icon = 'images/track.png'
var db_supported = window.openDatabase
var db = null
var media = {}
var debug = true
var max_rows_in_db = 10

//
// check to see if local dbs are supported by the browser
//
if (db_supported) {
	db = window.openDatabase("pyitunesweb", "1", "Py-iTunes-Web", 1024*1024)
	db.transaction(function(tx) {
		tx.executeSql('select * from recently_played limit 1', null, null, function(tx,error) {
			// database is not yet created
			create_db()
		})
	})
}

//
// create the local database
//
function create_db() {
	if (debug) 
		alert('create db')
	db.transaction(function(tx) {
		tx.executeSql('create table recently_played (src text,artist text,track text,album text)')
	})
}

//
// play a given track
//
media.play = function(src, artist, track, album) { 
	var fullsrc = PIT_PATH+"iTunes Music/"+src
	$('player').src = fullsrc
	$('player').load()
	$('player').play() 
	media.on_track_changed(src, artist, track, album) // NOTE: do not use fullsrc here as play() prepends PIT_PATH
}

//
// show a notification when a track has changed
//
media.on_track_changed = function(src, artist, track, album) {
	// show html5 notification
	if (window.webkitNotifications.checkPermission() == 0) {
		window.webkitNotifications.createNotification(icon, artist, track).show()
	} else {
		window.webkitNotifications.requestPermission();
	}
	// add track to recent list
	media.add_track_to_recently_played(src, artist, track, album)
}

//
// add this track to the recently played list
//
media.add_track_to_recently_played = function(src, artist, track, album) {
	if (db_supported) {
		db.transaction(function(tx) {
			tx.executeSql('insert into recently_played values (?,?,?,?)', [src,artist,track,album], media.chkdb, db_err)
		})
	}
}

//
// handles db errors
//
function db_err(tx,err) {
	alert(err.message)
}

//
// check that the db isn't getting too big
//
media.chkdb = function(tx,rs) {
	tx.executeSql('select count(*) as count from recently_played', null, function(tx,result) {
			count = result.rows.item(0).count
			if (count > max_rows_in_db) {
				// !!! Todo: implement
			}
	}, db_err)
}

//
// get recently played tracks
//
media.get_recently_played = function() {
	if (db_supported)	{
		db.transaction(function(tx) {
				tx.executeSql("select distinct * from recently_played limit 8", null, media.get_recently_played_callback, db_err)
		})
	} else {
		$('recentlyPlayed').style.display = 'none'
	}
}


//
// callback method for getting recently played tracks
//
media.get_recently_played_callback = function(tx,resultset) {
	var list = $('recentlyPlayedList')
	list.innerHTML = '' // clear previous tracks
	$('recentlyPlayed').style.display = 'block'
	for (var i=0; i<resultset.rows.length; i++) {
		row = resultset.rows.item(i)
		var li = document.createElement('li')
		var img = document.createElement('img')
		var a = document.createElement('a')
		a.href = "javascript:media.play('"+row.src+"','"+row.artist+"','"+row.track+"','"+row.album+"');"
		a.title = "Play '"+row.artist+" - "+row.track+"'"
		a.insertBefore(img)
		li.insertBefore(a)
		list.insertBefore(li)
		img.src = "images/track.png"
		img.className = "album"
		new Ajax.Request("ajax.cgi?method=artwork.get&artist="+row.artist+"&album="+row.album, {
				method: 'get',
				onSuccess: function(t) {
					json = t.responseText.evalJSON()
					debugger
					if (json.error) {
						if (debug)
							alert(json.error)
						this.img.src = "/images/track.png"
					} else {
						this.img.src = json.src
					}
				}.bind({img:img})
			}
		)
	}
	if (resultset.rows.length == 0) {
		$('recentlyPlayed').style.display = 'none'
	}
}

// # vim: sw=2 ts=2 cin ai
