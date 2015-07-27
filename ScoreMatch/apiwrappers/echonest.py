#!/usr/bin/python
# -*- coding: utf-8 -*-
from pyechonest import song
from pyechonest import song
from pyechonest import track

import json
import urllib
from pyechonest import config
from echonestsong import *



def search_echonest(song_artist, song_name):
    songs = song.search(artist=song_artist, title=song_name,
                        buckets=['id:7digital-US', 'tracks'])
    songresult = []
    for s in songs:
        ss_tracks = s.get_tracks('7digital-US')
        if ss_tracks != []:
            preview_url = ss_tracks[0].get('preview_url')
            title = s.title
            id = s.id
            e = EchonestSong(id, title, preview_url)
            tempo = s.audio_summary['tempo']
            duration = s.audio_summary['duration']
            timesig = s.audio_summary['time_signature']
            key = s.audio_summary['key']
            chroma = parse_echonest_analysisurl(s.audio_summary('analysis_url'))
            e.set_features(tempo, duration, timesig, key, chroma)
            songresult.append(e)
  
    return songresult
def get_echonest_features_for_file(audio_file):
    pytrack = track.track_from_filename(audio_file)
    
    chroma = parse_echonest_analysisurl(pytrack.analysis_url)
    return chroma,pytrack.time_signature,pytrack.key,pytrack.duration,pytrack.tempo
def get_echonest_features_for_file(url):
    pytrack = track.track_from_url(url)
    
    chroma = parse_echonest_analysisurl(pytrack.analysis_url)
    return chroma,pytrack.time_signature,pytrack.key,pytrack.duration,pytrack.tempo
def parse_echonest_analysisurl(url):
    print url
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    i = 0
    chroma = []
    for k in data['segments']:
        dur = k['duration']
        num_of_frames = int(dur /  config.echonest_window_time)
        pitches = k['pitches']
        chroma.extend([pitches,] * num_of_frames)   
    return chroma
def get_echonestsong_by_spotifyid(spotify_id):
    url = echonest_base + 'track/profile?api_key=' + api_key \
        + '&format=json&id=spotify:track:' + spotify_id \
        + '&bucket=audio_summary'
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    song_id = data['response']['track']['song_id']
    url = echonest_base + 'song/profile?api_key=' + api_key \
        + '&format=json&bucket=audio_summary&id=' + song_id
    print url
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    song = data['response']['songs'][0]
    title = song['title']
    audio_summary = song['audio_summary']
    tempo = audio_summary['tempo']
    duration = audio_summary['duration']
    timesig = audio_summary['time_signature']
    key = audio_summary['key']
    analysis_url = audio_summary['analysis_url']
    chroma = parse_echonest_analysisurl(analysis_url)

    try:
    	preview_url = audio_summary['preview_url']
    except KeyError:
    	preview_url = None
    e = EchonestSong(song_id, title, preview_url)
    e.set_features(tempo, duration, timesig, key,chroma)

    return e

api_key = 'KAPGNMBNAIKKXKWG7'

config.ECHO_NEST_API_KEY = api_key
echonest_base = 'http://developer.echonest.com/api/v4/'
search_echonest('radiohead', 'karma police')
#get_echonestsong_by_spotifyid('4C5YAL1hwwospGYk0SzvrJ')3
get_echonest_features_for_file("TeVasMilonga.wav")
