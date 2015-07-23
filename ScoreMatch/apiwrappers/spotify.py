#!/usr/bin/python
# -*- coding: utf-8 -*-

import spotipy
import sys
import pprint
import json
import urllib
import urlparse
from spotifytrack import *
spotify_base = 'https://api.spotify.com/v1/'
echonest_base = 'http://developer.echonest.com/api/v4/'


def parse_spotify_search(data):
    items = data['tracks']['items']
    tracks = []
    for i in range(len(items)):
        item = items[i]
        track_id = item['id']
        preview_url = item['preview_url']
        name = item['name']
        t = SpotifyTrack(track_id, name, preview_url)
        tracks.append(t)
    return tracks


def query_spotify(query):
    url = spotify_base + 'search?q=' + query + '&type=track&limit=10'
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return parse_spotify_search(data)
def parse_spotify_track(data):
    track_id = data['id']
    preview_url = data['preview_url']
    name = data['name']
    return SpotifyTrack(track_id, name, preview_url)
def create_spotify_track(id):
    url = spotify_base + 'tracks/'+id
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return parse_spotify_track(data)
def query(song_name, artist_name='', type='spotify'):
    if type == 'spotify':
        return querySpotify(song_name + ' ' + artist_name)

    return tracks

# query("hellrider","judas priest","echonest")
