# -*- coding: utf-8 -*- 
import spotipy
import sys
import pprint
import json
import urllib
import urlparse
from Track import *
spotify_base = "https://api.spotify.com/v1/"
echonest_base = "http://developer.echonest.com/api/v4/"
def parseSpotify(data):
	items = data['tracks']['items']
	tracks = []
	for i in range(len(items)):
		item = items[i]
		track_id=item['id']
		preview_url = item['preview_url']
		name = item['name']
		t = Track(track_id,name,preview_url)
		tracks.append(t)
	return tracks
def querySpotify(query):
	url = spotify_base + "search?q="+query+"&type=track&limit=10"
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	return parseSpotify(data)
# def searchEchonestSongs():
# 	api_key= "KAPGNMBNAIKKXKWG7"
# 	url = echonest_base + "song/search?api_key="+api_key+"&format=json&"+"title="+song_name
# 	if artist_name:
# 		url = url + "&artist="+artist_name
# 	print url
# 	response = urllib.urlopen(url)
# 	data = json.loads(response.read())	
# def getEchonestTracks(spotifyid):

# def parseEchonest(data):
# 	songs=data["response"]["songs"]
# 	for i in range(len(songs)):
# 		song=songs[i]
# 		track_id = song["id"]
# 		name = song
# def queryEchonest(song_name,artist_name=""):
# 	api_key= "KAPGNMBNAIKKXKWG7"
# 	url = echonest_base + "song/search?api_key="+api_key+"&format=json&"+"title="+song_name
# 	if artist_name:
# 		url = url + "&artist="+artist_name
# 	print url
# 	response = urllib.urlopen(url)
# 	data = json.loads(response.read())
# 	return parseEchonest(data)
def query(song_name,artist_name="",type="spotify"):
	if type=="spotify":
		return querySpotify(song_name+" "+artist_name)

	return tracks

#query("hellrider","judas priest","echonest")
