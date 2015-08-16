#!/usr/bin/python
# -*- coding: utf-8 -*-

from analyzable import *
import utils
from musicdatatype import MusicDataType
import os
from echonest import get_echonestsong_by_spotifyid
class SpotifyTrack(Analyzable):
    """
        This class represents a SpotifyTrack

    Attributes:
        id: Spotify id of the track

        name: name of the spotify track

        preview_url: preview_url of the spotify track

        uri: uri of the spotify track

        features: :class:`.EchonestFeatures` for the spotify track
    """
    def __init__(
        self,
        id,
        name,
        preview_url,
        uri,
        ):

        Analyzable.__init__(self, id)
        self.preview_url = preview_url
        self.name = name
        self.type = 'spotify'
        self.uri = uri

    def get_chromagram(self, mode=MusicDataType.AUDIO):
        """
        Get chromagram for the spotify track

        Creates chromagram either from mp3(:meth:`utils.get_chromagram_from_audio`) or echonest analysis (:meth:`apiwrappers.echonest.get_echonestsong_by_spotifyid`) of the spotify track.Chromagram may return None if there is no matching echonest song for the spotify track
        
        Args:
            mode: :class:`.MusicDataType`. either should be audio or echonest

        Returns:
            Chromagram representation.
        """
        directory = os.path.dirname(os.path.abspath(__file__))
        if mode == MusicDataType.AUDIO:
            audio_file_path = directory + '/' + self.id + '.mp3'
            utils.download_file(self.preview_url, audio_file_path)
            chromagram = get_chromagram_from_audio(audio_file_path)
            remove_file(audio_file_path)
            return chromagram
        elif mode == MusicDataType.ECHONEST:
            e = get_echonestsong_by_spotifyid(self.id)
            if e:
                self.echonest_features = e.features
                return e.features.chroma
        return None
