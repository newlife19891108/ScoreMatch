#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
from analyzable import *
import utils
from musicdatatype import MusicDataType
class EchonestSong(Analyzable):
    """Class representing an Echonest Song (in very basic way).

    Attributes:
        id: id of the Echonest Song.

        name: name of the Echonest Song.

        preview_url: preview_url of the Echonest Song.
        
        features: :class:`.EchonestFeatures` of EchonestSong.
    """
    def __init__(
        self,
        id,
        name,
        preview_url,artist
        ):

        Analyzable.__init__(self, id)
        self.preview_url = preview_url
        self.name = name
        self.type = 'echonest'
        self.artist = artist
        self.analysis_url = None
    def get_chromagram(self,mode=MusicDataType.AUDIO):

        directory = os.path.dirname(os.path.abspath(__file__))
        if mode == MusicDataType.AUDIO:
            audio_file_path = directory + '/' + self.id + '.mp3'
            utils.download_file(self.preview_url, audio_file_path)
            chromagram = utils.get_chromagram_from_audio(audio_file_path)
            utils.remove_file(audio_file_path)
            return chromagram
        elif mode == MusicDataType.ECHONEST:
            if  self.features:
                return self.features.chroma
            else:
                print "No echonest song found for:"+self.id
        return None

    def set_features(self, features):
        self.features = features
