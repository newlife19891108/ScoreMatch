#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    This module provides wrappers for required echonest api functions.
"""
from pyechonest import track

import json
import urllib
import config
from echonestsong import *
import hashlib
from connectionmanager import ConnectionManager
from connectionmanager import CheckInformation
from connectionsettings import ConnectionSettings
import numpy as np
from echonestfeatures import EchonestFeatures


def songs_by_artist_id(id):
    """Creates list of songs given an artist id

    Args:
        id: Echonest artist id
    Returns:
        A list of :class:`.EchonestSong` instances

    """

    songs = get_songs_for_artist(id)
    return songs


def get_data_by_md5(md5):
    """
        Get Echonest track profile data for the given md5

        Args:
            md5: target md5 values
        Returns:
            Track profile data as dict
    """

    base_url = echonest_base + 'track/profile?'
    params = {
        'api_key': api_key,
        'format': 'json',
        'bucket': 'audio_summary',
        'md5': md5,
        }
    data = ConnectionManager().get_data(base_url, params)
    return data


def check_file_exists(audio_file):
    """
        Checks if a file already uploaded to Echonest before

        Args:
            audio_file:path of the target audio file
        Returns:
            tuple (json data for the file,True if file already uploaded)
    """

    f = open(audio_file, 'rb')
    md5 = hashlib.md5(f.read()).hexdigest()
    data = get_data_by_md5(md5)
    return (data, data['response']['status']['message'] == 'Success')


def check_analysis_complete(track_id):
    """
        Checks if analysis of a track is ready on Echonest

        Args:
            track_id: track id of target track

        Returns:
            tuple(json data for the track profile)
    """

    base_url = echonest_base + 'track/profile?'
    params = {
        'api_key': api_key,
        'format': json,
        'bucket': audio_summary,
        'id': 'spotify:track:' + track_id,
        }
    ci = CheckInformation(*check_information_header
                          + 'Waiting for completion of analysis:'
                          + track_id)
    data = ConnectionManager().get_data(base_url, params, ci)

    return (data, data['response']['track']['status'] != 'pending')


def create_echonest_features(audio_summary):
    """
        Create set of echonest features from audio summary portion of Echonest API results

        Args:
            audio_summary:Dictionary of echonest features
        Returns:
            :class:`.EchonestFeatures` instance with extracted echonest features
    """

    chroma = parse_echonest_analysisurl(audio_summary['analysis_url'])
    audio_summary['chroma'] = chroma
    return EchonestFeatures(audio_summary)


def get_echonest_features_for_local_file(audio_file):
    """
        Get echonest features for a local audio file.

        It first checks if echonest analysis of the file already exists.
        If not audio file is uploaded to Echonest for further analysis

        Args:
            audio_file:path of audio file

        Returns:
            :class:`.EchonestFeatures` instance with extracted echonest features
    """

    print 'file checking'
    (data, file_exists) = check_file_exists(audio_file)
    audio_summary = data['response']['track']['audio_summary']

    if file_exists:
        print 'file exists!'
        return create_echonest_features(audio_summary)
    else:
        track_id = get_echonest_track_for_file(audio_file)
        (data, analysis_complete) = check_analysis_complete(track_id)
        return create_echonest_features(audio_summary)


def extract_artist_from_text(text):
    """
        Wrapper for Echonest's extractArtist method.

        Args:
            text: text to extract artists

        Returns:
            List of (artist id,artist name)
    """
    base_url = echonest_base + 'artist/extract?'
    params = {'api_key': api_key, 'format': 'json',
              'text': text.title()}
    ci = CheckInformation(*check_information_header
                          + ('Waiting for artist extraction from text: '
                           + text, ))
    data = ConnectionManager().get_data(base_url, params,
            check_information=ci)
    artists = data['response']['artists']
    artist_results = [(artist['id'], artist['name']) for artist in
                      artists]
    return artist_results


def get_echonest_track_for_file(audio_file):
    """
        Uploads an audio file to Echonest for acquiring its analysis later

        Args:
            audio_file: Path of audio file

        Returns:
            track id of uploaded file
    """
    print 'uploading', audio_file
    url = 'http://developer.echonest.com/api/v4/track/upload?'
    values = {'api_key': api_key, 'filetype': 'mp3'}
    ci = CheckInformation(keys=['response', 'status', 'message'],
                          expected_value='Success', wait_amount=5,
                          wait_text='Waiting for file upload:'
                          + audio_file)
    f = open(audio_file)
    data = ConnectionManager().post_data(url, f, values, ci)
    f.close()
    t_id = data['response']['track']['id']
    return t_id


def get_songs_for_artist(artist_id):

    """
        Get list of echonest songs for a given artist_id

        Args:
            artist_id: Echonest artist id

        Returns:
            List of :class:`.EchonestSong`

    """
    base_url = echonest_base + 'song/search?'
    params = (
        ('api_key', api_key),
        ('format', 'json'),
        ('results', '100'),
        ('artist_id', artist_id),
        ('bucket', 'id:7digital-US'),
        ('bucket', 'audio_summary'),
        ('bucket', 'tracks'),
        )
    ci = CheckInformation(*check_information_header
                          + ('Echonest search for artist id:'
                          + artist_id, ))
    data = ConnectionManager().get_data(base_url, params, ci)
    songs = data['response']['songs']

    echonest_songs = []
    for song in songs:
        tracks = song['tracks']
        preview_url = ''
        for t in tracks:
            preview_url = t['preview_url']
        e = EchonestSong(song['id'], song['title'], preview_url)
        echonest_songs.append(e)
    return echonest_songs


def parse_echonest_analysisurl(url):
    """
        Parse chroma from echonest analysis url of a track

        url: echonest analysis url

        Returns:
            12 dimensional chroma matrix
    """
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    chroma = []
    for k in data['segments']:
        dur = k['duration']
        num_of_frames = int(dur / config.echonest_window_time)
        pitches = k['pitches']
        chroma.extend([pitches] * num_of_frames)
    return np.array(chroma)


def get_echonestsong_by_spotifyid(spotify_id):
    """
        Get echonestsong for a given spotify track id

        spotify_id: spotify id of a spotify track

        Returns:
            :class:`.EchonestSong` if a song is found with specified foreign spotify id
            
            None if no song is found with spotify_id
    """
    url = echonest_base + 'track/profile?'
    params = {
        'api_key': api_key,
        'format': 'json',
        'id': 'spotify:track:' + spotify_id,
        'bucket': 'audio_summary',
        }
    wait_text = ('Waiting for echonest song for spotify id: '
                 + str(spotify_id), )
    ci = CheckInformation(*check_information_header + wait_text)
    ci2 = CheckInformation(['response', 'status', 'code'], 5, 65,
                           wait_text)
    print 'requesting'
    data = ConnectionManager().get_data(url, params,
            check_information=[ci, ci2])
    status_code = data['response']['status']['code']

    if status_code == 5 or status_code == 3:
        print 'no echonest song for spotify id:' + spotify_id
        return None
    elif status_code == 0:
        song_id = data['response']['track']['song_id']
        url = echonest_base + 'song/profile?'
        params = {
            'api_key': api_key,
            'format': 'json',
            'bucket': 'audio_summary',
            'id': song_id,
            }
        ci.wait_text = 'Waiting for song profile: ' + song_id
        data = ConnectionManager().get_data(url, params,
                check_information=ci)
        songs = data['response']['songs']
        if songs == []:
            return None
        song = songs[0]
        title = song['title']
        audio_summary = song['audio_summary']
        preview_url = (audio_summary['preview_url'] if 'preview_url'
                       in audio_summary.keys() else None)

        echonestfeatures = create_echonest_features(audio_summary)
        e = EchonestSong(song_id, title, preview_url)
        e.set_features(echonestfeatures)
        return e
    return None


check_information_header = (['response', 'status', 'message'], 'Success'
                            , 65)
echonest_base = ConnectionSettings().echonest_base
api_key = ConnectionSettings().echonest_key
