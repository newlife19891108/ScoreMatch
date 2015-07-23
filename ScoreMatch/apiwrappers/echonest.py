from pyechonest import song
from pyechonest import song

import json
import urllib
from pyechonest import config
from echonestsong import *
api_key = "KAPGNMBNAIKKXKWG7"

config.ECHO_NEST_API_KEY=api_key
echonest_base = 'http://developer.echonest.com/api/v4/'

def search_echonest(song_artist,song_name):
	songs =  song.search(artist=song_artist, title=song_name, buckets=['id:7digital-US', 'tracks'])
	songresult = []
	for s in songs:
		ss_tracks = s.get_tracks('7digital-US')
		if ss_tracks != []:
			preview_url = ss_tracks[0].get('preview_url')
			title = s.title
			id = s.id
			e = EchonestSong(id,title,preview_url)
			songresult.append(e)
	return songresult
def get_song_by_spotifyid(spotify_id):
	url = echonest_base + "track/profile?api_key="+api_key+"&format=json&id=spotify:track:"+spotify_id+ "&bucket=audio_summary"
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	print data['response']['track']['song_id']
	return 0
search_echonest("radiohead","karma police")
get_song_by_spotifyid("4C5YAL1hwwospGYk0SzvrJ")