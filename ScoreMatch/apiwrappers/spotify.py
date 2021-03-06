#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    This module provides wrappers for required spotify api functions.
"""
from connectionmanager import ConnectionManager
from spotifytrack import *
from connectionsettings import ConnectionSettings


def get_spotify_uri_by_id(spotify_id):

    """Get spotify uri for the given spotify id

    Returns:
        spotify uri
    """
    url = spotify_base + 'tracks/' + spotify_id
    data = ConnectionManager().get_data(url)
    return data['uri']


def songs_by_artist_name(artist):
    """Get list of spotify songs given an artist name

    Returns:
        List of :class:`.SpotifyTrack`
    """
    base_url = spotify_base + 'search?'
    params = {'q': artist, 'type': 'artist'}
    data = ConnectionManager().get_data(base_url, params)
    artists = data['artists']['items']
    artist_id = None
    for item in artists:
        artist_name = item['name']
        if artist_name.lower() == artist.lower():
            artist_id = item['id']
            return get_top_tracks_for_artist(artist_id)
    return []
def songs_by_artist_name2(artist):
    base_url = spotify_base + 'search?'
    params = {'q': artist, 'type': 'artist'}
    data = ConnectionManager().get_data(base_url, params)
    artists = data['artists']['items']
    artist_id = None
    markets = ['TR','ES','US']
    tracks = []
    for item in artists:
        artist_name = item['name']
        if artist_name.lower() == artist.lower():
            for market in markets:
                tracks.extend(get_songs_by_market(artist_name,market))
            return tracks
    return []
def get_songs_by_market(artist,market):
 
    base_url = spotify_base + 'search?'
    params = {'q': artist, 'type': 'track', 'market':market,'limit': '20'}
    data = ConnectionManager().get_data(base_url, params)
    tracks = data['tracks']['items']
    track_names = []
    for track in tracks:
        spotify_track = parse_spotify_track(track)
        track_names.append(spotify_track)
    return track_names
def get_top_tracks_for_artist(artist_id):
    """Get top tracks given an artist id

    Returns:
        List of :class:`.SpotifyTrack`

    """
    base_url = spotify_base + 'artists/' + artist_id + '/top-tracks?'
    params = {'country': 'US'}
    data = ConnectionManager().get_data(base_url, params)
    tracks = data['tracks']
    track_names = []
    for track in tracks:
        spotify_track = parse_spotify_track(track)
        track_names.append(spotify_track)
    return track_names


def query_spotify(query):
    """Query spotify with the given query

    Return:
        List of :class:`.SpotifyTrack`
    """
    if query == '':
        return []
    base_url = spotify_base + 'search?'
    params = {'q': query, 'type': 'track', 'limit': '50'}
    data = ConnectionManager().get_data(base_url, params)
    tracks = data['tracks']['items']
    track_names = []
    track_names_sub = []
    for track in tracks:
        spotify_track = parse_spotify_track(track)
        if utils.num_common_words(spotify_track.name,query)>0:
            track_names.append(spotify_track)
        track_names_sub.append(spotify_track)
    if len(track_names)>0:
        print len(track_names), 'found for', query.encode('utf-8')
        return track_names
    else:
        print len(track_names_sub), 'found for', query.encode('utf-8')
        return track_names_sub      

def parse_spotify_track(data):
    track_id = data['id']
    try:
        preview_url = data['preview_url']
    except KeyError, e:
        preview_url = ''
    name = data['name']
    uri = data['uri']
    artist = data['artists'][0]['name']
    return SpotifyTrack(track_id, name, preview_url, uri,artist)


def create_spotify_track(id):
    """Create a spotify track given an spotify id

    Returns:
        :class:`.SpotifyTrack` instance for given id
    """
    base_url = spotify_base + 'tracks/' + id
    data = ConnectionManager().get_data(base_url)
    return parse_spotify_track(data)


spotify_base = ConnectionSettings().spotify_base

# query("hellrider","judas priest","echonest")
