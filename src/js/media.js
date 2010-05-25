
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
		tx.executeSql('create table recently_played (src,artist,track)')
	})
}

//
// convenience methods
//
function $(elem) { 
	return document.getElementById(elem); 
}

//
// play a given track
//
media.play = function(src, artist, track) { 
	var fullsrc = PIT_PATH+"iTunes Music/"+src
	$('player').src = fullsrc
	$('player').load()
	$('player').play() 
	media.on_track_changed(fullsrc, artist, track)
}

//
// show a notification when a track has changed
//
media.on_track_changed = function(src, artist, track) {
	// show html5 notification
	if (window.webkitNotifications.checkPermission() == 0) {
		window.webkitNotifications.createNotification(icon, artist, track).show()
	} else {
		window.webkitNotifications.requestPermission();
	}
	// add track to recent list
	media.add_track_to_recently_played(src, artist, track)
}

//
// add this track to the recently played list
//
media.add_track_to_recently_played = function(src, artist, track) {
	if (db_supported) {
		db.transaction(function(tx) {
			tx.executeSql('insert into recently_played values (?,?,?)', [src,artist,track], media.chkdb, db_err)
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

// # vim: sw=2 ts=2 cin ai
